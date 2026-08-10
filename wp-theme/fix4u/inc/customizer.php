<?php
/**
 * Theme Customizer settings — editable at Appearance → Customize in /admin.
 *
 * @package Fix4u
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Register Customizer settings.
 *
 * @param WP_Customize_Manager $wp_customize Customizer.
 */
function fix4u_customize_register( $wp_customize ) {
	$wp_customize->add_panel(
		'fix4u_panel',
		array(
			'title'       => __( 'FIX4U Site Settings', 'fix4u' ),
			'description' => __( 'Manage branding, hero, contact, and hours for the FIX4U theme.', 'fix4u' ),
			'priority'    => 30,
		)
	);

	// Colors.
	$wp_customize->add_section(
		'fix4u_colors',
		array(
			'title' => __( 'Colors', 'fix4u' ),
			'panel' => 'fix4u_panel',
		)
	);

	$colors = array(
		'fix4u_primary_color'      => array( __( 'Primary color', 'fix4u' ), '#87CEEB' ),
		'fix4u_primary_dark'       => array( __( 'Primary dark', 'fix4u' ), '#5BC0DE' ),
		'fix4u_dark_color'         => array( __( 'Dark text / header', 'fix4u' ), '#2D3436' ),
	);

	foreach ( $colors as $id => $meta ) {
		$wp_customize->add_setting(
			$id,
			array(
				'default'           => $meta[1],
				'sanitize_callback' => 'sanitize_hex_color',
				'transport'         => 'refresh',
			)
		);
		$wp_customize->add_control(
			new WP_Customize_Color_Control(
				$wp_customize,
				$id,
				array(
					'label'   => $meta[0],
					'section' => 'fix4u_colors',
				)
			)
		);
	}

	// Hero EN.
	$wp_customize->add_section(
		'fix4u_hero_en',
		array(
			'title' => __( 'Hero (English)', 'fix4u' ),
			'panel' => 'fix4u_panel',
		)
	);

	fix4u_add_text_setting(
		$wp_customize,
		'fix4u_hero_title_en',
		__( 'Headline', 'fix4u' ),
		'fix4u_hero_en',
		'Your Devices, Our Expertise'
	);
	fix4u_add_text_setting(
		$wp_customize,
		'fix4u_hero_subtitle_en',
		__( 'Supporting text', 'fix4u' ),
		'fix4u_hero_en',
		'Professional phone & computer repair, instant trade-in, and quality used devices. Fast service, fair prices, guaranteed satisfaction.',
		'textarea'
	);
	fix4u_add_text_setting(
		$wp_customize,
		'fix4u_cta_label_en',
		__( 'CTA button label', 'fix4u' ),
		'fix4u_hero_en',
		'Get Quote'
	);

	// Hero ZH.
	$wp_customize->add_section(
		'fix4u_hero_zh',
		array(
			'title' => __( 'Hero (Chinese)', 'fix4u' ),
			'panel' => 'fix4u_panel',
		)
	);

	fix4u_add_text_setting(
		$wp_customize,
		'fix4u_hero_title_zh',
		__( 'Headline', 'fix4u' ),
		'fix4u_hero_zh',
		'您的设备，我们的专长'
	);
	fix4u_add_text_setting(
		$wp_customize,
		'fix4u_hero_subtitle_zh',
		__( 'Supporting text', 'fix4u' ),
		'fix4u_hero_zh',
		'专业手机与电脑维修、快速二手回收、高品质翻新设备。服务迅速、价格合理、质保无忧。',
		'textarea'
	);
	fix4u_add_text_setting(
		$wp_customize,
		'fix4u_cta_label_zh',
		__( 'CTA button label', 'fix4u' ),
		'fix4u_hero_zh',
		'获取报价'
	);

	// Contact.
	$wp_customize->add_section(
		'fix4u_contact',
		array(
			'title' => __( 'Contact details', 'fix4u' ),
			'panel' => 'fix4u_panel',
		)
	);

	fix4u_add_text_setting( $wp_customize, 'fix4u_phone', __( 'Phone', 'fix4u' ), 'fix4u_contact', '0800 800 349' );
	fix4u_add_text_setting( $wp_customize, 'fix4u_email_sales', __( 'Sales email', 'fix4u' ), 'fix4u_contact', 'info@fix4u.co.nz' );
	fix4u_add_text_setting( $wp_customize, 'fix4u_email_support', __( 'Support email', 'fix4u' ), 'fix4u_contact', 'support@fix4u.co.nz' );
	fix4u_add_text_setting( $wp_customize, 'fix4u_address', __( 'Address', 'fix4u' ), 'fix4u_contact', '1 Cebel Place, Rosedale, Auckland', 'textarea' );
	fix4u_add_text_setting( $wp_customize, 'fix4u_hours_weekday', __( 'Weekday hours', 'fix4u' ), 'fix4u_contact', '9:00 AM - 5:00 PM' );
	fix4u_add_text_setting( $wp_customize, 'fix4u_hours_weekend', __( 'Weekend hours', 'fix4u' ), 'fix4u_contact', 'Closed' );

	// Web design pricing.
	$wp_customize->add_section(
		'fix4u_pricing',
		array(
			'title' => __( 'Web design pricing', 'fix4u' ),
			'panel' => 'fix4u_panel',
		)
	);
	fix4u_add_text_setting( $wp_customize, 'fix4u_price_portal', __( 'Portal website from', 'fix4u' ), 'fix4u_pricing', 'From $899' );
	fix4u_add_text_setting( $wp_customize, 'fix4u_price_ecommerce', __( 'E-commerce from', 'fix4u' ), 'fix4u_pricing', 'From $1,899' );
}
add_action( 'customize_register', 'fix4u_customize_register' );

/**
 * Helper to register a text/textarea setting + control.
 *
 * @param WP_Customize_Manager $wp_customize Customizer.
 * @param string               $id           Setting ID.
 * @param string               $label        Label.
 * @param string               $section      Section ID.
 * @param string               $default      Default value.
 * @param string               $type         Control type.
 */
function fix4u_add_text_setting( $wp_customize, $id, $label, $section, $default, $type = 'text' ) {
	$wp_customize->add_setting(
		$id,
		array(
			'default'           => $default,
			'sanitize_callback' => ( 'textarea' === $type ) ? 'sanitize_textarea_field' : 'sanitize_text_field',
			'transport'         => 'refresh',
		)
	);
	$wp_customize->add_control(
		$id,
		array(
			'label'   => $label,
			'section' => $section,
			'type'    => $type,
		)
	);
}
