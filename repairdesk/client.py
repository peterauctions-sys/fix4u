"""Minimal RepairDesk Public API client (stdlib only)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_BASE_URL = "https://api.repairdesk.co/api/web/v1"
USER_AGENT = "FIX4U-RepairDesk-Client/1.0"


class RepairDeskError(RuntimeError):
    def __init__(self, message: str, status_code: int | None = None, payload: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class RepairDeskClient:
    """Client for RepairDesk web API v1.

    Auth: pass ``api_key`` or set ``REPAIRDESK_API_KEY``.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 60.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("REPAIRDESK_API_KEY", "")
        if not self.api_key:
            raise RepairDeskError("REPAIRDESK_API_KEY is required")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        query = {"api_key": self.api_key}
        if params:
            query.update({k: v for k, v in params.items() if v is not None})
        url = f"{self.base_url}{path}?{urllib.parse.urlencode(query)}"
        data = None if body is None else json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            method=method.upper(),
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                payload = json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                payload = {"raw": raw}
            raise RepairDeskError(
                f"HTTP {exc.code} for {method.upper()} {path}: {payload}",
                status_code=exc.code,
                payload=payload,
            ) from exc
        except urllib.error.URLError as exc:
            raise RepairDeskError(f"Network error: {exc}") from exc

        if isinstance(payload, dict) and payload.get("success") is False:
            raise RepairDeskError(
                payload.get("message") or "RepairDesk API returned success=false",
                status_code=payload.get("statusCode"),
                payload=payload,
            )
        return payload

    # --- Inventory ---

    def list_inventory(
        self,
        *,
        page: int = 1,
        pagesize: int = 100,
        keyword: str | None = None,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            "/inventory",
            params={"page": page, "pagesize": pagesize, "keyword": keyword},
        )

    def iter_inventory(
        self,
        *,
        keyword: str | None = None,
        pagesize: int = 100,
        max_pages: int | None = None,
    ):
        page = 1
        while True:
            payload = self.list_inventory(page=page, pagesize=pagesize, keyword=keyword)
            data = payload.get("data") or {}
            items = data.get("inventoryListData") or []
            for item in items:
                yield item
            pagination = data.get("pagination") or {}
            if not pagination.get("next_page_exist"):
                break
            page = int(pagination.get("next_page") or (page + 1))
            if max_pages is not None and page > max_pages:
                break

    def get_inventory(self, item_id: int | str) -> dict[str, Any]:
        return self._request("GET", f"/inventory/{item_id}")

    def update_inventory(self, item_id: int | str, fields: dict[str, Any]) -> dict[str, Any]:
        """Update inventory item content (name, description, notes, price, stock, …)."""
        body = dict(fields)
        body["id"] = int(item_id)
        return self._request("PUT", f"/inventory/{item_id}", body=body)

    def update_inventory_content(
        self,
        item_id: int | str,
        *,
        name: str | None = None,
        description: str | None = None,
        notes: str | None = None,
        price: float | None = None,
        in_stock: int | None = None,
        sku: str | None = None,
        preserve_pricing: bool = True,
    ) -> dict[str, Any]:
        """Safely update text/content fields while keeping price/stock unless overridden."""
        current = self.get_inventory(item_id).get("data") or {}
        payload: dict[str, Any] = {
            "name": name if name is not None else current.get("name"),
            "description": description if description is not None else (current.get("description") or ""),
            "notes": notes if notes is not None else (current.get("notes") or ""),
            "sku": sku if sku is not None else (current.get("sku") or ""),
            "tax_inclusive": int(current.get("tax_inclusive") or 1),
        }
        if price is not None:
            payload["price"] = float(price)
        elif preserve_pricing:
            retail = current.get("original_price") or (current.get("prices") or {}).get("retail_price")
            if retail not in (None, ""):
                payload["price"] = float(retail)

        if in_stock is not None:
            payload["in_stock"] = int(in_stock)
        elif preserve_pricing and current.get("in_stock") not in (None, ""):
            payload["in_stock"] = int(float(current["in_stock"]))

        tax = current.get("tax_class") or {}
        if tax.get("id"):
            payload["tax_class"] = int(tax["id"])

        cost = current.get("cost_price")
        if cost not in (None, ""):
            try:
                payload["cost_price"] = float(cost)
            except (TypeError, ValueError):
                pass

        return self.update_inventory(item_id, payload)

    def add_inventory(self, fields: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/inventory/addnewitem", body=fields)

    # --- Customers / tickets (read helpers) ---

    def list_customers(self, *, page: int = 1) -> dict[str, Any]:
        return self._request("GET", "/customers", params={"page": page})

    def update_customer(self, customer_id: int | str, fields: dict[str, Any]) -> dict[str, Any]:
        return self._request("PUT", f"/customers/{customer_id}", body=fields)

    def list_tickets(self, *, page: int = 1) -> dict[str, Any]:
        return self._request("GET", "/tickets", params={"page": page})

    def get_ticket(self, ticket_id: int | str) -> dict[str, Any]:
        return self._request("GET", f"/tickets/{ticket_id}")

    def update_ticket(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("PUT", "/ticket/updateticket", body=payload)

    # --- Used / refurbished helpers ---

    USED_KEYWORDS = (
        "Pre-owned",
        "Preowned",
        "Refurbished",
        "Used",
        "二手",
        "[Pre-owned]",
    )

    def list_used_devices(self, *, in_stock_only: bool = True) -> list[dict[str, Any]]:
        by_id: dict[str, dict[str, Any]] = {}
        for keyword in self.USED_KEYWORDS:
            for item in self.iter_inventory(keyword=keyword, pagesize=100):
                by_id[str(item["id"])] = item
        items = list(by_id.values())
        if in_stock_only:
            items = [i for i in items if float(i.get("in_stock") or 0) > 0]
        items.sort(key=lambda i: (i.get("name") or "").lower())
        return items
