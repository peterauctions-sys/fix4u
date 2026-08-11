<?php
/**
 * Front page (English home).
 *
 * @package Fix4u
 */

get_header();

$hero_title = fix4u_mod( 'fix4u_hero_title_en', 'Your Devices, Our Expertise' );
$hero_sub   = fix4u_mod( 'fix4u_hero_subtitle_en', 'Professional phone & computer repair, instant trade-in, and quality used devices. Fast service, fair prices, guaranteed satisfaction.' );
$phone      = fix4u_mod( 'fix4u_phone', '0800 800 349' );
$email_s    = fix4u_mod( 'fix4u_email_sales', 'info@fix4u.co.nz' );
$email_p    = fix4u_mod( 'fix4u_email_support', 'support@fix4u.co.nz' );
$address    = fix4u_mod( 'fix4u_address', '1 Cebel Place, Rosedale, Auckland' );
$hours_wd   = fix4u_mod( 'fix4u_hours_weekday', '9:00 AM - 5:00 PM' );
$hours_we   = fix4u_mod( 'fix4u_hours_weekend', 'Closed' );
$price_p    = fix4u_mod( 'fix4u_price_portal', 'From $899' );
$price_e    = fix4u_mod( 'fix4u_price_ecommerce', 'From $1,899' );
$hero_bg    = fix4u_img( 'hero.jpg' );
?>
<style>
.hero {
	background: linear-gradient(135deg, rgba(135, 206, 235, 0.9) 0%, rgba(227, 242, 253, 0.95) 100%),
		url('<?php echo esc_url( $hero_bg ); ?>') center/cover;
}
</style>

<section class="hero">
	<div class="container">
		<h1><?php echo esc_html( $hero_title ); ?></h1>
		<p><?php echo esc_html( $hero_sub ); ?></p>
		<div class="hero-btns">
			<a href="#services" class="btn btn-primary">Our Services</a>
			<a href="#contact" class="btn btn-outline">Contact Us</a>
		</div>
	</div>
</section>

<section id="services" class="services">
	<div class="container">
		<div class="section-header">
			<h2>Our Services</h2>
			<p>Everything you need for your devices</p>
		</div>
		<div class="services-grid">
			<?php
			$services = array(
				array( 'phone.jpg', 'Phone Repair', 'Professional repair services for all major brands', array( 'Screen Replacement', 'Battery Replacement', 'Water Damage Repair', 'Charging Port Fix', 'Speaker & Microphone' ) ),
				array( 'tablet.jpg', 'Tablet Repair', 'Professional tablet repair for all brands', array( 'Screen Replacement', 'Battery Replacement', 'Charging Port Fix', 'Water Damage Repair', 'Button Repair' ) ),
				array( 'watch.jpg', 'Watch Repair', 'Smartwatch and classic watch repairs', array( 'Screen Replacement', 'Battery Replacement', 'Band Replacement', 'Water Damage Repair', 'Software Issues' ) ),
				array( 'computer.jpg', 'Computer Repair', 'Expert repair for laptops and desktops', array( 'Screen Replacement', 'Battery Replacement', 'Keyboard Repair', 'Software Issues', 'Hardware Upgrades' ) ),
				array( 'tradein.jpg', 'Trade-In', 'Get instant cash for your old device', array( 'Instant Valuation', 'Any Condition Accepted', 'Fair Market Price', 'Quick Payment', 'Data Wipe Guarantee' ) ),
				array( 'used.jpg', 'Used Devices', 'Quality refurbished phones & computers', array( 'Used Phones', 'Laptops & Computers', 'Tested & Certified', '90-Day Warranty', 'Unlocked All Networks' ) ),
				array( 'webdesign.jpg', 'Web Services', 'Professional web design & development', array( 'Portal Websites', 'E-commerce Websites', 'Responsive Design', 'SEO Optimization', 'Domain & Hosting' ) ),
			);
			foreach ( $services as $svc ) :
				?>
				<div class="service-card">
					<img src="<?php echo esc_url( fix4u_img( $svc[0] ) ); ?>" alt="<?php echo esc_attr( $svc[1] ); ?>" class="service-img">
					<div class="service-content">
						<h3><?php echo esc_html( $svc[1] ); ?></h3>
						<p><?php echo esc_html( $svc[2] ); ?></p>
						<ul>
							<?php foreach ( $svc[3] as $item ) : ?>
								<li><?php echo esc_html( $item ); ?></li>
							<?php endforeach; ?>
						</ul>
					</div>
				</div>
			<?php endforeach; ?>
		</div>
	</div>
</section>

<section id="web-design" class="services" style="background: var(--light);">
	<div class="container">
		<div class="section-header">
			<h2>Web Design Services</h2>
			<p>Build your professional online presence</p>
		</div>
		<div class="services-grid">
			<div class="service-card">
				<div class="service-content">
					<h3>Portal Websites</h3>
					<p>Professional websites for your business</p>
					<ul>
						<li>Corporate Website Design</li>
						<li>Custom Branding</li>
						<li>SEO Optimization</li>
						<li>Contact Form Integration</li>
						<li>Mobile Responsive</li>
					</ul>
					<p style="margin-top: 15px; color: var(--primary); font-weight: 600;"><?php echo esc_html( $price_p ); ?></p>
				</div>
			</div>
			<div class="service-card">
				<div class="service-content">
					<h3>E-commerce Websites</h3>
					<p>Start your online business</p>
					<ul>
						<li>Online Store Setup</li>
						<li>Product Display & Cart</li>
						<li>Payment Gateway Integration</li>
						<li>Order Management</li>
						<li>Inventory System</li>
					</ul>
					<p style="margin-top: 15px; color: var(--primary); font-weight: 600;"><?php echo esc_html( $price_e ); ?></p>
				</div>
			</div>
		</div>
		<div style="text-align: center; margin-top: 50px;">
			<a href="#contact" class="btn btn-primary" style="padding: 15px 40px; font-size: 1.1rem;">Get Free Quote</a>
		</div>
	</div>
</section>

<section id="why-us" class="why-us">
	<div class="container">
		<div class="section-header">
			<h2>Why Choose FIX4U</h2>
			<p>We put customers first</p>
		</div>
		<div class="features-grid">
			<div class="feature-item"><h3>No Win, No Fee</h3><p>No cure, no pay - we only charge if we fix it</p></div>
			<div class="feature-item"><h3>3-Month Warranty</h3><p>3-month warranty on all repairs</p></div>
			<div class="feature-item"><h3>12-Month Battery Warranty</h3><p>12-month warranty on battery replacements</p></div>
			<div class="feature-item"><h3>Fast Service</h3><p>Most repairs done within 1 hour</p></div>
			<div class="feature-item"><h3>Fair Prices</h3><p>Competitive pricing, no hidden fees</p></div>
			<div class="feature-item"><h3>Expert Techs</h3><p>Certified repair specialists</p></div>
		</div>
	</div>
</section>

<section id="contact" class="contact">
	<div class="container">
		<div class="section-header">
			<h2>Contact Us</h2>
			<p>Get in touch for a free quote</p>
		</div>
		<div class="contact-grid">
			<div class="contact-info">
				<h3>Get In Touch</h3>
				<div class="contact-item">
					<span>📍</span>
					<div><strong>Location</strong><br><?php echo esc_html( $address ); ?></div>
				</div>
				<div class="contact-item">
					<span>📱</span>
					<div><strong>Phone</strong><br><a href="<?php echo esc_url( fix4u_phone_tel() ); ?>"><?php echo esc_html( $phone ); ?></a></div>
				</div>
				<div class="contact-item">
					<span>✉️</span>
					<div><strong>Sales</strong><br><a href="mailto:<?php echo esc_attr( $email_s ); ?>"><?php echo esc_html( $email_s ); ?></a></div>
				</div>
				<div class="contact-item">
					<span>🛠️</span>
					<div><strong>Support</strong><br><a href="mailto:<?php echo esc_attr( $email_p ); ?>"><?php echo esc_html( $email_p ); ?></a></div>
				</div>
			</div>
			<div class="contact-info">
				<h3>Business Hours</h3>
				<table class="hours-table">
					<tr><td>Monday - Friday</td><td><?php echo esc_html( $hours_wd ); ?></td></tr>
					<tr><td>Saturday - Sunday</td><td><?php echo esc_html( $hours_we ); ?></td></tr>
				</table>
			</div>
		</div>
	</div>
</section>
<?php
get_footer();
