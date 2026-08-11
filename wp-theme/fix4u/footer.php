<?php
/**
 * Footer template.
 *
 * @package Fix4u
 */

$is_zh = fix4u_is_zh();
?>
<footer>
	<div class="container">
		<div class="footer-content">
			<div class="footer-col">
				<h4>FIX4U</h4>
				<p style="color: #AAA;">
					<?php
					echo esc_html(
						$is_zh
							? '您在新西兰值得信赖的手机维修、二手回收与翻新设备合作伙伴。'
							: 'Your trusted partner for phone repair, trade-in, and quality used devices in New Zealand.'
					);
					?>
				</p>
			</div>
			<div class="footer-col">
				<h4><?php echo esc_html( $is_zh ? '服务' : 'Services' ); ?></h4>
				<a href="#services"><?php echo esc_html( $is_zh ? '手机维修' : 'Phone Repair' ); ?></a>
				<a href="#services"><?php echo esc_html( $is_zh ? '平板维修' : 'Tablet Repair' ); ?></a>
				<a href="#services"><?php echo esc_html( $is_zh ? '手表维修' : 'Watch Repair' ); ?></a>
				<a href="#services"><?php echo esc_html( $is_zh ? '电脑维修' : 'Computer Repair' ); ?></a>
				<a href="#services"><?php echo esc_html( $is_zh ? '设备回收' : 'Trade-In' ); ?></a>
				<a href="#services"><?php echo esc_html( $is_zh ? '二手设备' : 'Used Devices' ); ?></a>
				<a href="#web-design"><?php echo esc_html( $is_zh ? '网站设计' : 'Web Design' ); ?></a>
			</div>
			<div class="footer-col">
				<h4><?php echo esc_html( $is_zh ? '快捷链接' : 'Quick Links' ); ?></h4>
				<a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php echo esc_html( $is_zh ? '首页' : 'Home' ); ?></a>
				<a href="#contact"><?php echo esc_html( $is_zh ? '联系我们' : 'Contact' ); ?></a>
				<?php if ( current_user_can( 'edit_theme_options' ) ) : ?>
					<a href="<?php echo esc_url( admin_url() ); ?>"><?php esc_html_e( 'Admin', 'fix4u' ); ?></a>
					<a href="<?php echo esc_url( admin_url( 'customize.php' ) ); ?>"><?php esc_html_e( 'Customize theme', 'fix4u' ); ?></a>
				<?php endif; ?>
			</div>
		</div>
		<div class="footer-bottom">
			<p>&copy; <?php echo esc_html( gmdate( 'Y' ) ); ?> FIX4U. <?php echo esc_html( $is_zh ? '保留所有权利。' : 'All rights reserved.' ); ?></p>
		</div>
	</div>
</footer>
<?php wp_footer(); ?>
</body>
</html>
