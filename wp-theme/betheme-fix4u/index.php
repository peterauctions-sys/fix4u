<?php
/**
 * Fallback index — load parent BeTheme index for non-front pages.
 *
 * @package Betheme_Fix4u
 */

$parent_index = trailingslashit( get_template_directory() ) . 'index.php';
if ( file_exists( $parent_index ) ) {
	include $parent_index;
	return;
}

get_header();
?>
<main class="container" style="padding:140px 0 80px;">
	<?php if ( have_posts() ) : ?>
		<?php while ( have_posts() ) : ?>
			<?php the_post(); ?>
			<article <?php post_class(); ?>>
				<h1><?php the_title(); ?></h1>
				<div><?php the_content(); ?></div>
			</article>
		<?php endwhile; ?>
	<?php endif; ?>
</main>
<?php
get_footer();
