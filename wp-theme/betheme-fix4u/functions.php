<?php
/**
 * Betheme FIX4U Design — child theme of Betheme.
 * Built for preview via Appearance → Themes → Live Preview.
 * Do not activate on production until approved.
 *
 * @package Betheme_Fix4u
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'BETHEME_FIX4U_VERSION', '1.0.0' );
define( 'BETHEME_FIX4U_DIR', get_stylesheet_directory() );
define( 'BETHEME_FIX4U_URI', get_stylesheet_directory_uri() );

/**
 * Enqueue parent + design styles/scripts.
 */
function betheme_fix4u_assets() {
	// Parent BeTheme stylesheet (required for child themes).
	wp_enqueue_style(
		'betheme-parent',
		get_template_directory_uri() . '/style.css',
		array(),
		wp_get_theme( 'betheme' )->get( 'Version' )
	);

	wp_enqueue_style(
		'betheme-fix4u-design',
		BETHEME_FIX4U_URI . '/assets/css/design.css',
		array( 'betheme-parent' ),
		BETHEME_FIX4U_VERSION
	);

	wp_enqueue_script(
		'betheme-fix4u-design',
		BETHEME_FIX4U_URI . '/assets/js/design.js',
		array(),
		BETHEME_FIX4U_VERSION,
		true
	);
}
add_action( 'wp_enqueue_scripts', 'betheme_fix4u_assets', 20 );

/**
 * Admin notice when this design theme is active (should stay inactive until approved).
 */
function betheme_fix4u_admin_notice() {
	$theme = wp_get_theme();
	if ( 'betheme-fix4u' !== $theme->get_stylesheet() ) {
		return;
	}
	if ( ! current_user_can( 'switch_themes' ) ) {
		return;
	}
	?>
	<div class="notice notice-warning">
		<p>
			<strong><?php esc_html_e( 'Betheme FIX4U Design is active.', 'betheme-fix4u' ); ?></strong>
			<?php esc_html_e( 'This was built as a preview copy of BeTheme. Switch back to Betheme if this was not intentional.', 'betheme-fix4u' ); ?>
		</p>
	</div>
	<?php
}
add_action( 'admin_notices', 'betheme_fix4u_admin_notice' );

/**
 * Image helper.
 *
 * @param string $file Filename under assets/images.
 * @return string
 */
function betheme_fix4u_img( $file ) {
	return BETHEME_FIX4U_URI . '/assets/images/' . ltrim( $file, '/' );
}
