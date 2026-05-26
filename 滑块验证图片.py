#直接截取图片需要最新版的selenium
#【方案1:通过计算缺口最左侧离图片的X轴距离并多次移动滑块补齐缺口】
from PIL import Image, ImageChops
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
import random
#截取有缺口的图片
def get_img0(d1):
    time.sleep(1)
    c1=d1.find_element(By.CLASS_NAME,'geetest_canvas_img')          #定位图片元素位置
    c1.screenshot('geetest_canvas_img0.png')          #保存图片
    image_1=Image.open('geetest_canvas_img0.png').convert('L')         #灰度图
    return image_1
#获取滑块x轴移动距离
def get_movevalue(image_1,image_2,threshold:int):
    diff_img1=ImageChops.difference(image_1, image_2)       #像素差异图
    diff_array =np.array(diff_img1)             #转为二位数组
    diff_array[diff_array<threshold]=0          #小于阈值的区域赋值0(区域变为黑色，则缺口为亮白色)
    diff_img2=Image.fromarray(diff_array)       #转为Image对象(PIL)
    get_bbox=diff_img2.getbbox()                #getbbox的返回值为[x_min, y_min, x_max, y_max]
    if not get_bbox:
        print("未能检测到缺口，请调整阈值(threshold)")
    get_x=get_bbox[0]-1         #减小缺口边框造成的误差
    print(f'缺口位置:{get_x},边界框:{get_bbox}')
    return get_x
#调整鼠标移动轨迹
def action_movie(move_value:int,a1:ActionChains,element):
    x1=move_value/2
    y1 = random.uniform(-5.5, 5.5)          #鼠标随机y轴移动px
    a1.click_and_hold(element).perform()        # 一直按住鼠标
    a1.move_by_offset(x1, y1).perform()
    time.sleep(random.uniform(0.5,1))
    a1.move_by_offset(x1, y1).perform()
    time.sleep(random.uniform(0.3,0.5))
    a1.move_by_offset(-0.5, -0.5).perform()       #鼠标向左回调【y轴一定要向下移动，不然报错("网络不给力")】(后撤步)
    time.sleep(0.3)
    a1.release().perform()
    WebDriverWait(d1,3).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="登 录"]')))
    d1.find_element(By.XPATH, '//input[@value="登 录"]').click()       #点击登录按钮

try:
    d1=webdriver.Chrome()
    d1.maximize_window()
    d1.get('https://mis-toutiao-python.itheima.net/#/')
    d1.find_element(By.CLASS_NAME,'yzm_btn').click()    #单击“输入用户名点击获取验证码”框
    time.sleep(3)
    d1.find_element(By.CLASS_NAME,'geetest_radar_tip_content').click()      #单机“验证”按钮
    #等待加载验证图片
    WebDriverWait(d1,3).until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_canvas_slice.geetest_absolute')))
    # 等待按钮加载且能使用
    e1=WebDriverWait(d1,3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
    #截取没有缺口的验证图片
    d1.execute_script('document.querySelectorAll("canvas")[1].style="display: none"')           #隐藏拼图
    d1.execute_script('document.querySelectorAll("canvas")[2].style="display: block; opacity: 1"')      #修改网页验证图片的元素使网页图片显示没有缺口
    c2=d1.find_element(By.CLASS_NAME,'geetest_canvas_img')     #定位完整图片元素
    time.sleep(2)
    c2.screenshot('geetest_canvas_img1.png')
    image_2 = Image.open('geetest_canvas_img1.png').convert('L')  # 转为灰度图
    d1.execute_script('document.querySelectorAll("canvas")[2].style="display: none; opacity: 1"')       #显示缺口
    a1 = ActionChains(d1)  # 创建鼠标对象
    image_1=get_img0(d1)        #有缺口的图片
    get_x=get_movevalue(image_1,image_2,threshold=30)       #缺口位置
    action_movie(get_x,a1,e1)
except Exception as e:
    print(f"error:{e}")
#方案2接口位置行【】
 #d1.execute_script('document.querySelectorAll("canvas")[2].style="display:none;"')      #恢复图片元素原样
# except Exception as e:
#     print(f"error:{e}")


#【方案2:尝试通过比较图片像素差异判断验证是否图片吻合】      6.2，82473
#2025.11.21(多次调试认为移动滑块验证似乎没有严格的时间限制,y轴移动数值较大就能避开反检测)
# #实时截取移动滑块时的验证图片
# def get_img0(d1):
#     #d1.execute_script('document.querySelectorAll("canvas")[1].style="display:none;"')
#     time.sleep(1)
#     c1=d1.find_element(By.CLASS_NAME,'geetest_canvas_img')          #定位图片元素位置
#     c1.screenshot('geetest_canvas_img0.png')          #保存图片
#     image_1=Image.open('geetest_canvas_img0.png').convert('L')         #灰度图
#     return image_1

# #通过比较图片的像素差异来判断滑块是否吻合(threshold值小了滑块容易提前停下，大了错过缺口)
# def diff_image(image_1,image_2,threshold=82467):      #threshold值越小，判断越严格(与滑块每次移动距离相关，还要多次调试程序得到准确率最高的值)
#     # 计算图片像素差异值
#     diff=ImageChops.difference(image_1,image_2)
#     diff_value=sum(diff.getdata())
#     return diff_value < threshold

#接2
 #截取没有缺口的验证图片
# d1.execute_script('document.querySelectorAll("canvas")[1].style="display: none"')           #隐藏拼图
# d1.execute_script('document.querySelectorAll("canvas")[2].style="display: block; opacity: 1"')      #修改网页验证图片的元素使网页图片显示没有缺口
# c2=d1.find_element(By.CLASS_NAME,'geetest_canvas_img')     #定位完整图片元素
# time.sleep(2)
# c2.screenshot('geetest_canvas_img1.png')
# d1.execute_script('document.querySelectorAll("canvas")[1].style="display: block; opacity: 1"')        #显示拼图
#image_2=Image.open('geetest_canvas_img1.png').convert('L')      #转为灰度图：利于比较验证图片是否吻合
#     y1 = random.uniform(-5.5, 5.5)          #添加鼠标y轴抖动(多次调试后发现数值大点才有用)
#     a1.move_by_offset(85, y1).perform()         #从px开始移动滑块，减少移动路径(估计缺口最近位置)
#     for i in range(32):         #最多移动32次(验证图片宽度为260px)
#         image_1 = get_img0(d1)  # 移动一次截取一次验证图片
#         if diff_image(image_1, image_2):  # 判断验证图片是否吻合
#             print('验证成功')
#             break
#         #(需要同时兼顾滑块移动距离和threshold值:滑动每次移动距离大了不容易吻合缺口)
#         a1.move_by_offset(6.4,y1).perform()       #滑块每次移动()px
#         time.sleep(random.uniform(0.3, 0.5))
#     time.sleep(0.3)
#     a1.release().perform()
# except Exception as e:
#     print(f"error:{e}")



#【废弃方案3:依次拖动滑块验证(耗时长，容易报错，不推荐)】
# for i in range(90,260,5):
#     a1.reset_actions()
#     a1.drag_and_drop_by_offset(e1,i,0).perform()
#     time.sleep(random.uniform(0,3))
#     try:
#         a2=WebDriverWait(d1,3).until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_reset_tip_content')))
#         a2.click()
#         a1.reset_actions()
#         time.sleep(random.uniform(0, 2))
#         e1=WebDriverWait(d1, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
#         a1.click_and_hold(e1).perform()
#     except:
#         continue






