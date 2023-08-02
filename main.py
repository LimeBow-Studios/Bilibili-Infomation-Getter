import os
import shutil

import requests
from nicegui import ui
import func

place_holder_img = 'https://dummyimage.com/1920x1080/666666/cccccc.png&text=点刷新'
image_url = ''
title_text = ''


def do_convert(what):
    def convert(num, what):
        try:
            func.convert(str(num), what)
        except Exception as e:
            with ui.dialog() as dialog_convert_err, ui.card():
                ui.label("转换失败！发生错误。{0}".format(str(e)))
                ui.button("好", on_click=dialog_convert_err.close)
            dialog_convert_err.open()
        try:
            if what == 'av2bv':
                bv_input.value = str(func.convert(str(num), what))
            elif what == 'bv2av':
                av_input.value = str(func.convert(str(num), what))
            else:
                pass
            with ui.dialog() as dialog_convert_ok, ui.card():
                ui.label("转换成功！文本框已更新。")
                ui.button("好", on_click=dialog_convert_ok.close)
            dialog_convert_ok.open()
        finally:
            ui.notify('转换中...', type="positive")

    bv_input_str = bv_input.value
    av_input_str = av_input.value
    if what == 'av2bv':
        convert(av_input_str, what)
    elif what == 'bv2av':
        convert(bv_input_str, what)
    else:
        pass


with ui.stepper().props('vertical').classes('w-full') as stepper:
    with ui.step('读取视频信息'):
        title_label = ui.label("请输入AV号。或者你可以输入BV号转AV号。")

        with ui.column():
            with ui.row():
                bv_input = ui.input("BV号", value="BV1GJ411x7h7").props(
                    'outlined clearable clear-icon="close" debounce="2000"')
                with bv_input.add_slot("prepend"):
                    ui.icon("comment")

                btn_convert_bv_to_av = ui.button("转换BV号到AV号", on_click=lambda: do_convert('bv2av')).props(
                    'color="primary" icon="checkbox" stack debounce="2000"')

            with ui.row():
                av_input = ui.input("AV号", value="av80433022").props(
                    'outlined clearable clear-icon="close"')
                with av_input.add_slot("prepend"):
                    ui.icon("comment")

                btn_convert_av_to_bv = ui.button("转换AV号到BV号", on_click=lambda: do_convert('av2bv')).props(
                    'color="primary" icon="checkbox" stack debounce="2000"')


        def step1_next():
            av = av_input.value
            bv = bv_input.value
            if (av is None) or (bv is None):
                stepper.previous()
                ui.notify('AV号或BV号为空！', type='warning')
            else:
                global image_url, title_text
                image_url, title_text = func.get_video_information(av, bv)
                stepper.next()
                ui.notify('第一步已完成！', type='positive')


        with ui.stepper_navigation():
            ui.button('下一步', on_click=step1_next)

    with ui.step('确认视频信息'):
        def refresh():
            def cache_img(url):
                # 发送GET请求下载图片
                response = requests.get(url)

                # 检查响应状态码
                if response.status_code == 200:
                    # 获取图片文件名
                    image_filename = os.path.basename(image_url)

                    # 指定缓存目录
                    cache_directory = 'cache'

                    # 创建缓存目录（如果不存在）
                    if not os.path.exists(cache_directory):
                        os.makedirs(cache_directory)

                    # 拼接图片的本地路径
                    image_path = os.path.join(cache_directory, image_filename)

                    # 保存图片到缓存目录
                    with open(image_path, 'wb') as f:
                        f.write(response.content)

                    print('图片已下载到缓存目录：', image_path)
                    return image_path
                else:
                    print('下载图片失败')
                    return place_holder_img

            cached_img = cache_img(image_url)

            video_pic.set_content(
                '<img src="{0}" style="width: 80%; height: auto;">'.format('./' + cached_img)
            )
            video_label1.set_text('视频标题: ' + title_text)
            video_label2.set_text('封面链接: ' + image_url)
            ui.notify('已刷新！', type='negative')


        def del_cache():
            try:
                shutil.rmtree('cache')
                ui.notify('缓存删除成功！', type='positive')
            except:
                ui.notify('没有可删除的缓存。', type='warning')


        with ui.card().tight():
            video_pic = ui.html('<img src="{0}" style="width: 80%; height: auto;">'.format(place_holder_img))
            with ui.card_section():
                with ui.column():
                    video_label1 = ui.label('视频标题: ' + title_text)
                    video_label2 = ui.label('封面链接: ' + image_url)

        with ui.stepper_navigation():
            with ui.row():
                ui.button("刷新信息", on_click=lambda: refresh()).props(
                    'color="primary" debounce="2000"')
                ui.button("删除缓存", on_click=lambda: shutil.rmtree('cache')).props(
                    'color="primary" debounce="2000"')
                ui.button('下一步', on_click=stepper.next)
                ui.button('返回', on_click=stepper.previous).props('flat')

    with ui.step('Bake'):
        ui.label('Bake for 20 minutes')
        with ui.stepper_navigation():
            with ui.row():
                ui.button('完成', on_click=lambda: ui.notify('Yay!', type='positive'))
                ui.button('返回', on_click=stepper.previous).props('flat')

# 启动
ui.run()
