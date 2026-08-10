<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<?php
$is_zh = fix4u_is_zh();
$home  = home_url( '/' );
$zh    = home_url( '/zh/' );
$en_cta = fix4u_mod( 'fix4u_cta_label_en', 'Get Quote' );
$zh_cta = fix4u_mod( 'fix4u_cta_label_zh', '获取报价' );
?>
<header>
	<div class="container">
		<nav>
			<a href="<?php echo esc_url( $is_zh ? $zh : $home ); ?>" class="logo">FIX<span>4U</span></a>
			<?php
			$menu_location = $is_zh ? 'primary_zh' : 'primary';
			if ( has_nav_menu( $menu_location ) ) {
				wp_nav_menu(
					array(
						'theme_location' => $menu_location,
						'container'      => false,
						'menu_class'     => 'nav-links',
						'fallback_cb'    => false,
						'depth'          => 1,
					)
				);
			} else {
				?>
				<ul class="nav-links">
					<?php if ( $is_zh ) : ?>
						<li><a href="#services">服务项目</a></li>
						<li><a href="#web-design">网站设计</a></li>
						<li><a href="#why-us">为什么选我们</a></li>
						<li><a href="#contact">联系我们</a></li>
						<li><a href="<?php echo esc_url( $home ); ?>" class="lang-btn">English</a></li>
					<?php else : ?>
						<li><a href="#services">Services</a></li>
						<li><a href="#web-design">Web Design</a></li>
						<li><a href="#why-us">Why Us</a></li>
						<li><a href="#contact">Contact</a></li>
						<li><a href="<?php echo esc_url( $zh ); ?>" class="lang-btn">中文</a></li>
					<?php endif; ?>
				</ul>
				<?php
			}
			?>
			<a href="#contact" class="cta-btn"><?php echo esc_html( $is_zh ? $zh_cta : $en_cta ); ?></a>
		</nav>
	</div>
</header>
