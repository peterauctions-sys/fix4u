<?php
/**
 * Theme helpers.
 *
 * @package Fix4u
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Get a theme mod with default fallback.
 *
 * @param string $key     Mod key.
 * @param string $default Default.
 * @return string
 */
function fix4u_mod( $key, $default = '' ) {
	$value = get_theme_mod( $key, $default );
	return ( null === $value || '' === $value ) ? $default : $value;
}

/**
 * Whether the current view should use Chinese copy.
 *
 * @return bool
 */
function fix4u_is_zh() {
	if ( is_page_template( 'templates/page-zh.php' ) ) {
		return true;
	}

	$lang = get_query_var( 'fix4u_lang' );
	if ( 'zh' === $lang ) {
		return true;
	}

	$path = isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '';
	if ( false !== strpos( $path, '/zh' ) || false !== strpos( $path, 'index-zh' ) ) {
		return true;
	}

	return false;
}

/**
 * Theme image URL.
 *
 * @param string $filename Image file under assets/images.
 * @return string
 */
function fix4u_img( $filename ) {
	return FIX4U_URI . '/assets/images/' . ltrim( $filename, '/' );
}

/**
 * Phone tel: href.
 *
 * @return string
 */
function fix4u_phone_tel() {
	$phone = fix4u_mod( 'fix4u_phone', '0800 800 349' );
	$digits = preg_replace( '/\D+/', '', $phone );
	return 'tel:+64' . ltrim( $digits, '0' );
}
