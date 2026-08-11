<?php
/**
 * Main index template.
 *
 * @package Fix4u
 */

get_header();
?>
<main class="container" style="padding:140px 0 80px;">
	<?php if ( have_posts() ) : ?>
		<?php while ( have_posts() ) : ?>
			<?php the_post(); ?>
			<article <?php post_class(); ?> style="margin-bottom:40px;">
				<h1><?php the_title(); ?></h1>
				<div><?php the_content(); ?></div>
			</article>
		<?php endwhile; ?>
	<?php else : ?>
		<p><?php esc_html_e( 'No content found.', 'fix4u' ); ?></p>
	<?php endif; ?>
</main>
<?php
get_footer();
