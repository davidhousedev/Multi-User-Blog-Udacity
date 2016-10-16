module.exports = function(grunt) {

  grunt.initConfig({
    cssmin: {
        target: {
            files: [{
                'static/dist/form.min.css': [
                             'static/main.css',
                             'static/form.css',],
                'static/dist/viewpost.min.css': [
                             'static/main.css',
                             'static/form.css',
                             'static/comments.css',
                             'static/blog_posts.css'],
                'static/dist/allblogs.min.css': [
                             'static/main.css',
                             'static/blog_posts.css'],
            }],
        },
    },
    watch: {
        files: ['static/*.css'],
        tasks: ['cssmin'],
        options: {
            interrupt: true,
        },
    },
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-cssmin');

  grunt.registerTask('default',[
        'cssmin'
    ]);
};