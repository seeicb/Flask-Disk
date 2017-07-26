// 文件上传
jQuery(function () {
    var $ = jQuery,
        $list = $('#thelist'),
        $btn = $('#ctlBtn'),
        state = 'pending',
        uploader;

    var log = (function () {
        var dom = $('#log');

        return function (str) {
            dom.append('<p>' + str + '</p>')
        }
    })();
    uploader = WebUploader.create({

        // 不压缩image
        resize: false,

        formData: {
            csrf_token: csrftoken

        },
        // 文件接收服务端。
        server: '',
        fileNumLimit: 10,
        fileSizeLimit: 1024 * 1024 * 1024,    // 1024 M
        fileSingleSizeLimit: 1024 * 1024 * 1024, // 1024 M

        // 选择文件的按钮。可选。
        // 内部根据当前运行是创建，可能是input元素，也可能是flash.
        pick: '#picker'
    });

    // 当有文件被添加进队列的时候
    uploader.on('fileQueued', function (file) {
        $list.append('<div id="' + file.id + '" class="item">' +
            '<h4 class="info">' + file.name + '</h4>' +
            '<p class="state">等待上传...</p>' +
            '</div>');
    });


    // 文件上传过程中创建进度条实时显示。
    uploader.on('uploadProgress', function (file, percentage) {
        var $li = $('#' + file.id),
            $percent = $li.find('.progress .progress-bar');

        // 避免重复创建
        if (!$percent.length) {
            $percent = $('<div class="progress progress-striped active">' +
                '<div class="progress-bar" role="progressbar" style="width: 0%">' +
                '</div>' +
                '</div>').appendTo($li).find('.progress-bar');
        }
        $li.find('p.state').text('上传中');

        $percent.css('width', percentage * 100 + '%');
    });

    uploader.on('uploadSuccess', function (file) {
        $('#' + file.id).find('p.state').text('已上传');
    });

    uploader.on('uploadError', function (file) {
        $('#' + file.id).find('p.state').text('上传出错');
    });

    uploader.on('uploadComplete', function (file) {
        $('#' + file.id).find('.progress').fadeOut();
    });


    uploader.on('all', function (type) {
        if (type === 'startUpload') {
            state = 'uploading';
        } else if (type === 'uploadFinished') {
            state = 'done';
        }

    });

    $btn.on('click', function () {
        uploader.upload();
    });


        uploader.onError = function( code ) {
            alert('错误:'+code);
        };
});
