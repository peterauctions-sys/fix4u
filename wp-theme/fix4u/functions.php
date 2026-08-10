<?php
/**
 * FIX4U theme functions.
 *
 * @package Fix4u
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'FIX4U_VERSION', '1.0.0' );
define( 'FIX4U_DIR', get_template_directory() );
define( 'FIX4U_URI', get_template_directory_uri() );

require_once FIX4U_DIR . '/inc/customizer.php';
require_once FIX4U_DIR . '/inc/helpers.php';

/**
 * Theme setup.
 */
function fix4u_setup() {
	load_theme_textdomain( 'fix4u', FIX4U_DIR . '/languages' );

	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support(
		'html5',
		array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script' )
	);
	add_theme_support(
		'custom-logo',
		array(
			'height'      => 80,
			'width'       => 240,
			'flex-height' => true,
			'flex-width'  => true,
		)
	);

	register_nav_menus(
		array(
			'primary'    => __( 'Primary Menu (English)', 'fix4u' ),
			'primary_zh' => __( 'Primary Menu (Chinese)', 'fix4u' ),
			'footer'     => __( 'Footer Menu', 'fix4u' ),
		)
	);
}
add_action( 'after_setup_theme', 'fix4u_setup' );

/**
 * Enqueue scripts and styles.
 */
function fix4u_scripts() {
	wp_enqueue_style(
		'fix4u-main',
		FIX4U_URI . '/assets/css/main.css',
		array(),
		FIX4U_VERSION
	);

	$primary      = sanitize_hex_color( get_theme_mod( 'fix4u_primary_color', '#87CEEB' ) );
	$primary_dark = sanitize_hex_color( get_theme_mod( 'fix4u_primary_dark', '#5BC0DE' ) );
	$dark         = sanitize_hex_color( get_theme_mod( 'fix4u_dark_color', '#2D3436' ) );

	$custom_css = sprintf(
		':root{--primary:%1$s;--primary-dark:%2$s;--dark:%3$s;}',
		$primary ? $primary : '#87CEEB',
		$primary_dark ? $primary_dark : '#5BC0DE',
		$dark ? $dark : '#2D3436'
	);
	wp_add_inline_style( 'fix4u-main', $custom_css );

	wp_enqueue_script(
		'fix4u-main',
		FIX4U_URI . '/assets/js/main.js',
		array(),
		FIX4U_VERSION,
		true
	);
}
add_action( 'wp_enqueue_scripts', 'fix4u_scripts' );

/**
 * Admin: quick links to manage theme via /admin.
 */
function fix4u_admin_menu() {
	add_theme_page(
		__( 'FIX4U Theme Guide', 'fix4u' ),
		__( 'FIX4U Theme', 'fix4u' ),
		'edit_theme_options',
		'fix4u-theme-guide',
		'fix4u_render_theme_guide'
	);
}
add_action( 'admin_menu', 'fix4u_admin_menu' );

/**
 * Theme guide page in wp-admin.
 */
function fix4u_render_theme_guide() {
	if ( ! current_user_can( 'edit_theme_options' ) ) {
		return;
	}

	$customize = admin_url( 'customize.php' );
	$menus     = admin_url( 'nav-menus.php' );
	$pages     = admin_url( 'edit.php?post_type=page' );
	?>
	<div class="wrap">
		<h1><?php esc_html_e( 'FIX4U Theme', 'fix4u' ); ?></h1>
		<p><?php esc_html_e( 'Manage this theme from WordPress admin (https://fix4u.co.nz/admin).', 'fix4u' ); ?></p>
		<ul style="list-style:disc;margin-left:1.5em;line-height:1.8;">
			<li><a href="<?php echo esc_url( $customize ); ?>"><?php esc_html_e( 'Appearance → Customize', 'fix4u' ); ?></a> — <?php esc_html_e( 'colors, hero text, phone, email, address, hours', 'fix4u' ); ?></li>
			<li><a href="<?php echo esc_url( $menus ); ?>"><?php esc_html_e( 'Appearance → Menus', 'fix4u' ); ?></a> — <?php esc_html_e( 'primary / Chinese / footer navigation', 'fix4u' ); ?></li>
			<li><a href="<?php echo esc_url( $pages ); ?>"><?php esc_html_e( 'Pages', 'fix4u' ); ?></a> — <?php esc_html_e( 'assign Front Page and Chinese Home page template', 'fix4u' ); ?></li>
		</ul>
		<p>
			<a class="button button-primary" href="<?php echo esc_url( $customize ); ?>"><?php esc_html_e( 'Open Customizer', 'fix4u' ); ?></a>
			<a class="button" href="<?php echo esc_url( home_url( '/' ) ); ?>" target="_blank" rel="noopener"><?php esc_html_e( 'View site', 'fix4u' ); ?></a>
		</p>
	</div>
	<?php
}

/**
 * Admin bar shortcut to Customizer / theme guide.
 *
 * @param WP_Admin_Bar $wp_admin_bar Admin bar.
 */
function fix4u_admin_bar( $wp_admin_bar ) {
	if ( ! current_user_can( 'edit_theme_options' ) ) {
		return;
	}

	$wp_admin_bar->add_node(
		array(
			'id'    => 'fix4u-theme',
			'title' => 'FIX4U Theme',
			'href'  => admin_url( 'themes.php?page=fix4u-theme-guide' ),
		)
	);
	$wp_admin_bar->add_node(
		array(
			'parent' => 'fix4u-theme',
			'id'     => 'fix4u-customize',
			'title'  => __( 'Customize', 'fix4u' ),
			'href'   => admin_url( 'customize.php' ),
		)
	);
}
add_action( 'admin_bar_menu', 'fix4u_admin_bar', 80 );

/**
 * After theme switch, nudge admins to Customizer via /admin.
 *
 * @param string $old_name Old theme name.
 */
function fix4u_after_switch_theme( $old_name ) {
	set_transient( 'fix4u_theme_activated', 1, MINUTE_IN_SECONDS * 5 );
}
add_action( 'after_switch_theme', 'fix4u_after_switch_theme' );

/**
 * Activation admin notice.
 */
function fix4u_activation_notice() {
	if ( ! get_transient( 'fix4u_theme_activated' ) ) {
		return;
	}
	if ( ! current_user_can( 'edit_theme_options' ) ) {
		return;
	}
	delete_transient( 'fix4u_theme_activated' );
	?>
	<div class="notice notice-success is-dismissible">
		<p>
			<strong><?php esc_html_e( 'FIX4U theme activated.', 'fix4u' ); ?></strong>
			<?php esc_html_e( 'Manage colors, hero, and contact details here:', 'fix4u' ); ?>
			<a href="<?php echo esc_url( admin_url( 'customize.php' ) ); ?>"><?php esc_html_e( 'Appearance → Customize', 'fix4u' ); ?></a>
			|
			<a href="<?php echo esc_url( admin_url( 'themes.php?page=fix4u-theme-guide' ) ); ?>"><?php esc_html_e( 'Theme guide', 'fix4u' ); ?></a>
		</p>
	</div>
	<?php
}
add_action( 'admin_notices', 'fix4u_activation_notice' );
