<?php
/**
 * Template Name: FIX4U Chinese Home
 * Template Post Type: page
 *
 * Chinese homepage — create a Page titled "中文" or "zh", assign this template,
 * then set its URL slug to `zh` so it lives at /zh/.
 *
 * @package Fix4u
 */

get_header();

$hero_title = fix4u_mod( 'fix4u_hero_title_zh', '您的设备，我们的专长' );
$hero_sub   = fix4u_mod( 'fix4u_hero_subtitle_zh', '专业手机电脑维修、快速回收、高品质二手设备。服务快捷、价格合理、质量保证。' );
$phone      = fix4u_mod( 'fix4u_phone', '0800 800 349' );
$email_s    = fix4u_mod( 'fix4u_email_sales', 'info@fix4u.co.nz' );
$email_p    = fix4u_mod( 'fix4u_email_support', 'support@fix4u.co.nz' );
$address    = fix4u_mod( 'fix4u_address', '1 Cebel Place, Rosedale, Auckland' );
$hours_wd   = fix4u_mod( 'fix4u_hours_weekday', '9:00 AM - 5:00 PM' );
$hours_we   = fix4u_mod( 'fix4u_hours_weekend', 'Closed' );
$price_p    = fix4u_mod( 'fix4u_price_portal', 'From $899' );
$price_e    = fix4u_mod( 'fix4u_price_ecommerce', 'From $1,899' );
$hero_bg    = fix4u_img( 'hero-zh.jpg' );
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
			<a href="#services" class="btn btn-primary">服务项目</a>
			<a href="#contact" class="btn btn-outline">联系我们</a>
		</div>
	</div>
</section>

<section id="services" class="services">
	<div class="container">
		<div class="section-header">
			<h2>服务项目</h2>
			<p>您的设备所需的一切</p>
		</div>
		<div class="services-grid">
			<?php
			$services = array(
				array( 'phone.jpg', '手机维修', '各品牌手机专业维修服务', array( '屏幕更换', '电池更换', '进水维修', '充电口维修', '扬声器与麦克风' ) ),
				array( 'tablet.jpg', '平板维修', '各品牌平板电脑专业维修', array( '屏幕更换', '电池更换', '充电口维修', '进水维修', '按键维修' ) ),
				array( 'watch.jpg', '手表维修', '智能手表和传统手表维修', array( '屏幕更换', '电池更换', '表带更换', '进水维修', '软件问题' ) ),
				array( 'computer.jpg', '电脑维修', '笔记本电脑和台式机专业维修', array( '屏幕更换', '电池更换', '键盘维修', '软件问题', '硬件升级' ) ),
				array( 'tradein.jpg', '设备回收', '旧设备快速变现', array( '即时估价', '任何成色均可', '公平市场价格', '快速付款', '数据清除保证' ) ),
				array( 'used.jpg', '二手设备', '高品质翻新手机和电脑', array( '二手手机', '笔记本与电脑', '检测认证', '90天质保', '全网通解锁' ) ),
				array( 'webdesign.jpg', '网站服务', '专业网站设计与开发服务', array( '门户网站', '电商网站', '响应式设计', 'SEO优化', '域名与主机' ) ),
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
			<h2>网站服务</h2>
			<p>打造专业在线形象，助力业务增长</p>
		</div>
		<div class="services-grid">
			<div class="service-card">
				<div class="service-content">
					<h3>门户网站</h3>
					<p>为您的企业打造专业形象的网站</p>
					<ul>
						<li>企业网站设计</li>
						<li>品牌定制</li>
						<li>SEO优化</li>
						<li>联系表单集成</li>
						<li>移动端适配</li>
					</ul>
					<p style="margin-top: 15px; color: var(--primary); font-weight: 600;"><?php echo esc_html( $price_p ); ?></p>
				</div>
			</div>
			<div class="service-card">
				<div class="service-content">
					<h3>电商网站</h3>
					<p>开启您的在线销售业务</p>
					<ul>
						<li>在线商店搭建</li>
						<li>商品展示与购物车</li>
						<li>支付网关集成</li>
						<li>订单管理</li>
						<li>库存系统</li>
					</ul>
					<p style="margin-top: 15px; color: var(--primary); font-weight: 600;"><?php echo esc_html( $price_e ); ?></p>
				</div>
			</div>
		</div>
		<div style="text-align: center; margin-top: 50px;">
			<a href="#contact" class="btn btn-primary" style="padding: 15px 40px; font-size: 1.1rem;">获取免费报价</a>
		</div>
	</div>
</section>

<section id="why-us" class="why-us">
	<div class="container">
		<div class="section-header">
			<h2>为什么选择 FIX4U</h2>
			<p>我们以客户为中心</p>
		</div>
		<div class="features-grid">
			<div class="feature-item"><h3>修不好不收费</h3><p>修好才收费，修不好不收钱</p></div>
			<div class="feature-item"><h3>3个月质保</h3><p>所有维修提供3个月质保</p></div>
			<div class="feature-item"><h3>电池12个月质保</h3><p>电池更换提供12个月质保</p></div>
			<div class="feature-item"><h3>快速服务</h3><p>多数维修1小时内完成</p></div>
			<div class="feature-item"><h3>价格合理</h3><p>价格透明，无隐藏费用</p></div>
			<div class="feature-item"><h3>专业技师</h3><p>认证维修专家</p></div>
		</div>
	</div>
</section>

<section id="contact" class="contact">
	<div class="container">
		<div class="section-header">
			<h2>联系我们</h2>
			<p>获取免费报价</p>
		</div>
		<div class="contact-grid">
			<div class="contact-info">
				<h3>联系方式</h3>
				<div class="contact-item">
					<span>📍</span>
					<div><strong>地址</strong><br><?php echo esc_html( $address ); ?></div>
				</div>
				<div class="contact-item">
					<span>📱</span>
					<div><strong>电话</strong><br><a href="<?php echo esc_url( fix4u_phone_tel() ); ?>"><?php echo esc_html( $phone ); ?></a></div>
				</div>
				<div class="contact-item">
					<span>✉️</span>
					<div><strong>销售</strong><br><a href="mailto:<?php echo esc_attr( $email_s ); ?>"><?php echo esc_html( $email_s ); ?></a></div>
				</div>
				<div class="contact-item">
					<span>🛠️</span>
					<div><strong>支持</strong><br><a href="mailto:<?php echo esc_attr( $email_p ); ?>"><?php echo esc_html( $email_p ); ?></a></div>
				</div>
			</div>
			<div class="contact-info">
				<h3>营业时间</h3>
				<table class="hours-table">
					<tr><td>周一至周五</td><td><?php echo esc_html( $hours_wd ); ?></td></tr>
					<tr><td>周六至周日</td><td><?php echo esc_html( $hours_we ); ?></td></tr>
				</table>
			</div>
		</div>
	</div>
</section>
<?php
get_footer();
