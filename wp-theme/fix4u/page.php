<?php
/**
 * Default page template.
 *
 * @package Fix4u
 */

get_header();
?>
<main class="container" style="padding:140px 0 80px;">
	<?php while ( have_posts() ) : ?>
		<?php the_post(); ?>
		<article <?php post_class(); ?>>
			<h1><?php the_title(); ?></h1>
			<div><?php the_content(); ?></div>
		</article>
	<?php endwhile; ?>
</main>
<?php
get_footer();
