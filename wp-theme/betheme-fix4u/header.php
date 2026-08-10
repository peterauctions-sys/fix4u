<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<?php wp_head(); ?>
</head>
<body <?php body_class( 'betheme-fix4u-design' ); ?>>
<?php wp_body_open(); ?>
<header>
	<div class="container">
		<nav>
			<a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="logo">FIX<span>4U</span></a>
			<ul class="nav-links">
				<li><a href="#services">Services</a></li>
				<li><a href="#web-design">Web Design</a></li>
				<li><a href="#why-us">Why Us</a></li>
				<li><a href="#contact">Contact</a></li>
			</ul>
			<a href="#contact" class="cta-btn">Get Quote</a>
		</nav>
	</div>
</header>
