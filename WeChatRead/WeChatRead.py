# -*- encoding: utf-8 -*-
#python>=3.6
'''
@File    :   WeChatRead.py
@Time    :   2025/01/07 17:39:48
@Author  :   sunyan
@Version :   1.0
@email   :   c_yansun
@Desc    :   从微信阅读中提取书本内容
'''
# here put the import lib
import codecs
import time
from time import sleep
from BaseInfo import BaseInfo
from selenium_qti7 import selenium_qti
import base64
import io
from PIL import Image

BIC = BaseInfo().base_info_dict
chrome_handle_dict = {}

def SaveImage(base64_image):
    '''
    @Time    :   2025/01/15 15:44:32
    @功能    :   保存canvas中获得的图片
    '''
    # 处理Base64编码的图片
    if base64_image:
        # 去掉DataURL的前缀
        image_data = base64_image.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # 保存图片到文件
        with open('canvas_image.png', 'wb') as f:
            f.write(image_bytes)
        
        # 或者使用PIL库处理图片
        image = Image.open(io.BytesIO(image_bytes))
        image.show()
    pass
# SaveImage("data:image/png;base64,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vfqGF+z8l8Mv1+sPQNyngLTDtGO1X2SffonzrcuLnNtdqdafgD51AVkvExddI7EaefU8jPsN/8Vlv4xfdecpCkgbtX3l7MeW17q8+zn2dw13vfrAcz4BUUAO+D8O3poAAQIECBAgcAiBTAVktV/7hf7zI6Jd37H65KFdo9F+Gf2W4dOJTQ8q3LeArI77bsty8SUR0Z730a6haH/acdo1Cu2C7t8brsdYz2HqAjIuE5tupbvpPBg/Tf6yp5OPf37fnacqIG2Wdr3LY4Y7d7V52p/2VbL2yU97Bkh7vsmnKSCH+NffexIgQIAAAQIE5hfYp4DMP+VpHLHdWrZ9QuJ2sKeRlykJECBAgAABAgSOIKCATIP+BsMtc69ZXpdy4/DJyTTv7F0IECBAgAABAgQIFBJQQK4e5utHxGcMF81/ZkT80NXf0jsQIECAAAECBAgQqCmggFw913a72B9YPpyw3SHruyLif67+lt6BAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgRFIcxzAAAY3ElEQVQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE0BBaRmrrYiQIAAAQIECBAgkFJAAUkZi6EIECBAgAABAgQI1BRQQGrmaisCBAgQIECAAAECKQUUkJSxGIoAAQIECBAgQIBATQEFpGautiJAgAABAgQIECCQUkABSRmLoQgQIECAAAECBAjUFFBAauZqKwIECBAgQIAAAQIpBRSQlLEYigABAgQIECBAgEBNAQWkZq62IkCAAAECBAgQIJBSQAFJGYuhCBAgQIAAAQIECNQUUEBq5morAgQIECBAgAABAikFFJCUsRiKAAECBAgQIECAQE2B/wMRliOkBlERdgAAAABJRU5ErkJggg==")

def GetwereadQQBookAllUrl(qti,  begin_url, save_file, begin_index=None, max_url_length=None):
    '''
    @Time    :   2025/01/07 13:09:12
    @功能    :   获得微信读书中，某本书的所有的url
    '''
    qti.browser.get(begin_url)
    url_list = []
    while 1:
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        if next_handle is None:
            break
        next_handle.click()
        sleep(1)
        url_list.append(qti.browser.current_url)
        if max_url_length is not None and len(url_list) == max_url_length:
            break
        pass

    with codecs.open(save_file, "w", "utf-8") as fw:
        fw.write("\n".join(url_list))
    pass

def GetwereadQQBookAllUrlV2(qti,  begin_url, save_file, begin_index=0, max_url_length=None):
    '''
    @Time    :   2025/01/07 13:09:12
    @功能    :   获得微信读书中，某本书的所有的url
    '''
    qti.browser.get(begin_url)
    if begin_index == 0:
        with codecs.open(save_file, "a+", "utf-8") as fw:
            fw.write(f"{begin_index};{begin_url}\n")
        begin_index = 1
    index, url_list =begin_index, []
    while 1:
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        if next_handle is None: break
        next_handle.click()
        sleep(1)
        url_list.append(qti.browser.current_url)
        with codecs.open(save_file, "a+", "utf-8") as fw:
            fw.write(f"{index};{qti.browser.current_url}\n")
        index += 1
        if max_url_length is not None and len(url_list) == max_url_length:
            break
    return 

def GetwereadQQBookAllUrlV3(qti,  begin_url, save_file, begin_index=0, max_url_length=None):
    '''
    @Time    :   2025/01/07 13:09:12
    @功能    :   获得微信读书中，某本书的所有的url
    这里需要区分：下一页和下一章的区别，从现有的目录结构来看下一章需要切换url，但是下一页不需要切换url
    '''
    qti.browser.get(begin_url)
    if begin_index == 0:
        with codecs.open(save_file, "a+", "utf-8") as fw:
            fw.write(f"{begin_index};{begin_url}\n")
        begin_index = 1
    index, url_list =begin_index, []
    while 1:
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        if next_handle is None: break
        update_url = True
        if next_handle.text.strip() == "下一页":
            update_url = False
        next_handle.click()
        sleep(1)
        url_list.append(qti.browser.current_url)
        with codecs.open(save_file, "a+", "utf-8") as fw:
            if not update_url:
                fw.write(f"{index};同一章节，下一页\n")
            else:
                fw.write(f"{index};{qti.browser.current_url}\n")
        index += 1
        if max_url_length is not None and len(url_list) == max_url_length:
            break
    return 

def MainDemo():
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    
    '''

    # qti = selenium_qti(
    #                    url='https://weread.qq.com/web/reader/a57325c05c8ed3a57224187',
    #                    chromedriver_path=BIC['chromedriver_path'])
    # qti.OpenChrome()
    # 下一章
    # # next_handle = qti.GetHandle(".//self::button[@class='readerFooter_button']")
    # next_handle = qti.GetHandles(xpath=".//self::div[@class='renderTarget_pager']//button")[1].click()
    # next_handle.click()
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Cookie":"wr_avatar=; wr_fp=2426543452; wr_gid=296512876; wr_vid=914251122; wr_rt=web%40ZxXPwZxXQT9ft4HpyvT_AL; wr_localvid=36d32d708367e5d7236d613; wr_name=%E5%BE%AE%E4%BF%A1%E7%94%A8%E6%88%B7; wr_gender=0; wr_pf=NaN; wr_skey=jz3HBZfZ"
    }
    url = "https://weread.qq.com/web/reader/a57325c05c8ed3a57224187k8f132430178f14e45fce0f7"
    # qti = selenium_qti(
    #                    url='https://weread.qq.com/web/reader/a57325c05c8ed3a57224187',
    #                    chromedriver_path=BIC['chromedriver_path'])
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/web/reader/a57325c05c8ed3a57224187',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                       debug=False)
    qti.OpenChrome()

    begin_url = "https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180"
    save_file = "url_list.txt"
    GetwereadQQBookAllUrl(qti, begin_url, save_file)

    with codecs.open(save_file, "r", "utf-8") as fr:
        lines = fr.readlines()
    
    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    // 存储绘制的文本内容及其位置信息
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });

    // 调用原始方法继续正常渲染
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    // 存储绘制的文本内容及其位置信息
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });

    // 调用原始方法继续正常渲染
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    // 按照 y 坐标排序，模拟自然阅读顺序
    const sortedText = capturedText.sort((a, b) => {
        // 首先按 y 坐标排序
        if (Math.abs(a.y - b.y) > 10) { // 允许 10px 的误差范围
            return a.y - b.y;
        }
        // y 坐标相近时按 x 坐标排序
        return a.x - b.x;
    });

    // 将文本内容提取出来
    return sortedText.map(item => item.text).join(' ');
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};
'''
    
    print(canvas_info)
    for index in range(len(lines)):
    # for index, line in enumerate(lines):
        # 注入js之后需要更换页面内容才可以使用 getCapturedText 获得最新的内容，因此需要向上翻一页之后再点击下一章才可以获得当前章节内容
        # 所以url才需要向下面一样向上取一个
        if index == 0:  url = begin_url
        else:           url =  lines[index-1].strip()
        qti.browser.get(url)
        # 注入js
        qti.browser.execute_script(script)
        # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        if next_handle is None:
            break
        next_handle.click()
        # 获取内容
        canvas_info = qti.browser.execute_script("return getCapturedText();")

        # 清除捕获的文本内容
        qti.browser.execute_script("clearCapturedText();")

        # 恢复原始方法
        qti.browser.execute_script("restoreOriginalMethods();")


    # 打开微信读书网页版并登录
    qti.browser.get(url)

    # # 等待用户手动登录完成

    # # 关闭浏览器
    # qti.browser.quit()

    # import io
    # import base64
    # from PIL import Image
    # canvas = qti.GetHandles(xpath=".//self::canvas")
    # canvas_base64 = qti.browser.execute_script("return arguments[0].toDataURL('image/png').substring(22);", canvas[0])
    # image_bytes = base64.b64decode(canvas_base64)
    # image = Image.open(io.BytesIO(image_bytes))
    # # 保存图像到本地文件
    # image.save('canvas_image.png')


    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    // 存储绘制的文本内容及其位置信息
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });

    // 调用原始方法继续正常渲染
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    // 存储绘制的文本内容及其位置信息
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });

    // 调用原始方法继续正常渲染
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    // 按照 y 坐标排序，模拟自然阅读顺序
    const sortedText = capturedText.sort((a, b) => {
        // 首先按 y 坐标排序
        if (Math.abs(a.y - b.y) > 10) { // 允许 10px 的误差范围
            return a.y - b.y;
        }
        // y 坐标相近时按 x 坐标排序
        return a.x - b.x;
    });

    // 将文本内容提取出来
    return sortedText.map(item => item.text).join(' ');
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};
'''
    # 注入js
    qti.browser.execute_script(script)
    
    # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容

    # 获取内容
    canvas_info = qti.browser.execute_script("return getCapturedText();")

    # 清除捕获的文本内容
    qti.browser.execute_script("clearCapturedText();")

    # 恢复原始方法
    qti.browser.execute_script("restoreOriginalMethods();")

    print(canvas_info)
    # 获得所有的章节url列表
 
    qti.Close()

def 微信读书Main(begin_url, book_name=None):
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    该函数只能获取所有已经绘制在canvas中的文本内容，
    以及穿插在文本中的上传的图片
    '''
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                    #    virtual_chrome=True, # 使用虚拟浏览器
                       debug=False)
    qti.OpenChrome()
    # qti.OpenBaseChrome(virtual_browser=True)
    # 最大化浏览器窗口
    qti.browser.maximize_window()

    if book_name is None:
        time_str = time.strftime('%Y_%m_%d',time.localtime(time.time()))
        book_name = f"微信阅读_{time_str}"

    save_file = rf"{BIC['base_path']}\url_list_{book_name}.txt"
    save_book = rf"{BIC['base_path']}\{book_name}.txt"

    try:
        # 中途异常退出
        with codecs.open(save_file, "r", "utf-8") as fr:
            url_lines = fr.readlines()
    except:
        # 首次执行
        url_lines = []

    qti.browser.get(begin_url)
    sleep(5)
    # 使用包含类名 isHorizontalReader 的 XPath 定位元素
    # 类中包含 isHorizontalReader 表示处于双页阅读；isNormalReader 表示处于滚动阅读
    read_model_handle = qti.GetHandle(".//self::button[contains(@class, 'isHorizontalReader')]")
    if read_model_handle is not None:
        read_model_handle.click()
    # # 如果要获得目录的标题需要先展开目录才行
    # qti.Click(".//self::button[@class='readerControls_item catalog']")
    # sleep(1)
    # 获取目录数量. 包含匹配的方式获取
    begin_index = 0
    # if url_lines == []:
    #     GetwereadQQBookAllUrlV2(qti, begin_url, save_file, begin_index=begin_index)
    # else:
    #     contents_handles = qti.GetHandles(".//self::li[contains(@class, 'readerCatalog_list_item')]")
    #     # for index, content in enumerate(contents_handles):
    #     #     # 如果没有登录账号，那么只能获取免费的目录
    #     #     print(f"{index}; {content.text}") #content.text 需要先展开书的目录
    #     if contents_handles is not None:
    #         # 获取书所有的章节url
    #         last_url = url_lines[-1].split(";")[-1].strip()
    #         begin_index = len(url_lines)

    #     if begin_index != len(contents_handles):
    #         GetwereadQQBookAllUrlV2(qti, last_url, save_file, begin_index=begin_index)

    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法， 在调用时将文本内容及其位置、样式等信息存储到 capturedText 数组中，然后调用原始的 fillText 方法。
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline,
            fontSize: this.font.split('px')[0], // 字体大小
            lineHeight: this.font.split('px')[0] * 1.2, // 行高
            textWidth: this.measureText(text).width, // 文本宽度
            textLines: text.split('\\n').length // 文本行数
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法，功能与 fillText 方法类似，将文本内容及其相关信息存储到 capturedText 数组中，然后调用原始的 strokeText 方法。
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    debugger
    console.log(capturedText)
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let contents_arr = [];
    let lastY = null;
    let last_style = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 40) {
            result += '\\n'; // 插入换行符
            //result += "YYY:"+lastY+'\\n'; // 插入换行符
            contents_arr.push({
                "Y":lastY,
                "content":result,
                "item":last_style
            })
            result = ""
        }
        result += item.text + '';
        lastY = item.y;
        last_style = item
    });
    if (result !== "" && last_style !== null){
        contents_arr.push({
            "Y":lastY,
            "content":result,
            "item":last_style
        })
    }
    

    // return result.trim();
    return contents_arr
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''

#     script = '''
# // 存储捕获的文本内容和矩形框信息
# let capturedText = [];
# let capturedRects = [];

# // 保存原始的 fillText, strokeText 和 rect 方法
# const originalFillText = CanvasRenderingContext2D.prototype.fillText;
# const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
# const originalRect = CanvasRenderingContext2D.prototype.rect;

# // 重写 fillText 方法
# CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
#     capturedText.push({
#         text: text,
#         x: x,
#         y: y,
#         maxWidth: maxWidth,
#         type: 'fill',
#         style: {
#             font: this.font,
#             fillStyle: this.fillStyle,
#             textAlign: this.textAlign,
#             textBaseline: this.textBaseline,
#             fontSize: this.font.split('px')[0], // 字体大小
#             lineHeight: this.font.split('px')[0] * 1.2, // 行高
#             textWidth: this.measureText(text).width, // 文本宽度
#             textLines: text.split('\\n').length // 文本行数
#         }
#     });
#     return originalFillText.apply(this, arguments);
# };

# // 重写 strokeText 方法
# CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
#     capturedText.push({
#         text: text,
#         x: x,
#         y: y,
#         maxWidth: maxWidth,
#         type: 'stroke',
#         style: {
#             font: this.font,
#             strokeStyle: this.strokeStyle,
#             textAlign: this.textAlign,
#             textBaseline: this.textBaseline
#         }
#     });
#     return originalStrokeText.apply(this, arguments);
# };

# // 重写 rect 方法
# CanvasRenderingContext2D.prototype.rect = function(x, y, width, height) {
#     capturedRects.push({
#         x: x,
#         y: y,
#         width: width,
#         height: height,
#         type: 'rect',
#         isRounded: false, // 默认为非圆角矩形
#         style: {
#             strokeStyle: this.strokeStyle,
#             fillStyle: this.fillStyle,
#             lineWidth: this.lineWidth
#         }
#     });
#     return originalRect.apply(this, arguments);
# };

# // 获取捕获的文本内容和矩形框信息
# window.getCapturedTextAndRects = function() {
#     const sortedText = capturedText.sort((a, b) => {
#         if (Math.abs(a.y - b.y) > 10) {
#             return a.y - b.y;
#         }
#         return a.x - b.x;
#     });

#     let result = '';
#     let contents_arr = [];
#     let lastY = null;
#     let last_style = null;
#     sortedText.forEach(item => {
#         if (lastY !== null && Math.abs(item.y - lastY) > 40) {
#             result += '\\n'; // 插入换行符
#             contents_arr.push({
#                 "Y": lastY,
#                 "content": result,
#                 "item": last_style
#             });
#             result = "";
#         }
#         result += item.text + '';
#         lastY = item.y;
#         last_style = item;
#     });
#     if (result !== "" && last_style !== null) {
#         contents_arr.push({
#             "Y": lastY,
#             "content": result,
#             "item": last_style
#         });
#     }

#     return {
#         text: contents_arr,
#         rects: capturedRects
#     };
# };

# // 清除已捕获的文本内容和矩形框信息
# window.clearCapturedTextAndRects = function() {
#     capturedText = [];
#     capturedRects = [];
# };

# // 恢复原始方法
# window.restoreOriginalMethods = function() {
#     CanvasRenderingContext2D.prototype.fillText = originalFillText;
#     CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
#     CanvasRenderingContext2D.prototype.rect = originalRect;
# };
# '''

    img_script='''
// function getAllImgs(){
window.getAllImgs = function(){
    // 获取 <img> 元素
    const imgElement = document.getElementsByTagName('img');

    let imgs = []
    for(let handle of imgElement){
        const classes = handle.className;
        // width60 wr_absolute wr_readerImage_opacity
        // width80 wr_absolute wr_readerImage_opacity
        if (classes.indexOf("wr_absolute wr_readerImage_opacity") ===-1)continue
        console.log("className",classes)
        // 获取坐标和长宽信息
        const rect = handle.getBoundingClientRect();
        const imgWidth = rect.width;
        const imgHeight = rect.height;
        const imgTop = rect.top;
        const imgLeft = rect.left;

        // 输出信息
        console.log(`Width: ${imgWidth}, Height: ${imgHeight}`);
        console.log(`Top: ${imgTop}, Left: ${imgLeft}`);

        // 获取样式信息
        const style = handle.style;
        

        // 解析坐标和尺寸
        const transform = style.transform;
        const width = style.width;
        const height = style.height;

        // 提取坐标值
        const translateX = transform.match(/translate\((\d+)px, (\d+)px\)/)[1];
        const translateY = transform.match(/translate\((\d+)px, (\d+)px\)/)[2];

        console.log(`X坐标: ${translateX}px`);
        console.log(`Y坐标: ${translateY}px`);
        console.log(`宽度: ${width}`);
        console.log(`高度: ${height}`);
        imgs.push({
        "src":handle.src,
        "X坐标":parseInt(translateX),
        "Y坐标":parseFloat(translateY),
        "宽度":width,
        "高度":height,
        "className":classes,
        })
    }
    return imgs
}
'''

    # 获得已经存储的book的最后一个章节位置
    try:
        with codecs.open(save_book, "r", "utf-8") as fr:
            book_lines = fr.readlines()
        begin = int(book_lines[-1].split(r"\t")[0].strip())
    except:
        begin = 0

    # 再读一次完整的url——list
    with codecs.open(save_file, "r", "utf-8") as fr:
        url_lines = fr.readlines()
    book_content = []
    try:
        for index in range(begin, len(url_lines)):
        # for index, line in enumerate(url_lines):
            # 注入js之后需要更换页面内容才可以使用 getCapturedText 获得最新的内容，因此需要向上翻一页之后再点击下一章才可以获得当前章节内容
            # 所以url才需要向下面一样向上取一个
            # if index == 0:  url = begin_url
            if index == 0:  url = url_lines[index+1].split(";")[-1].strip()
            else:           url =  url_lines[index].split(";")[-1].strip()
            qti.browser.get(url)
            sleep(5)
            # 注入js
            qti.browser.execute_script(script)
            if index == 0:
                # 首页需要使用点击上一章才能获取完整
                next_handle = qti.GetHandle(xpath=".//self::button[@class='readerHeaderButton']")
            else:
                # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
                next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
            if next_handle is None:
                break
            next_handle.click()
            sleep(5)
            # 获取内容
            qti.browser.execute_script(img_script) #注入获取图片的脚本
            canvas_info = qti.browser.execute_script("return getCapturedText();")
            dynamic_web_content = 循环获得已经渲染到网页的动态内容(qti)
            img_dict_list = qti.browser.execute_script("return getAllImgs();")
            new_canvas_info = {data_dict["Y"]:data_dict["content"] for data_dict in canvas_info}
            new_img_dict = {int(img_dict['Y坐标']):img_dict for img_dict in img_dict_list}
            combined_sorted_keys = sorted(list(new_canvas_info.keys()) + list(new_img_dict.keys()))
            new_content = []
            for key in combined_sorted_keys:
                if key in list(new_canvas_info.keys()):
                    new_content.append(new_canvas_info[key])
                else:
                    new_content.append(f"{str(new_img_dict[key])}\n")
                    pass
            canvas_info = "".join(new_content)
            if dynamic_web_content.strip() != "":
                canvas_info = f"{canvas_info}\n{dynamic_web_content}"
            print(canvas_info)
            book_content.append(canvas_info)
            with codecs.open(save_book, "a+", "utf-8") as fa:
                fa.write(f"{canvas_info}\n{index+1}\t\n")
            # 清除捕获的文本内容
            qti.browser.execute_script("clearCapturedText();")

            # 恢复原始方法
            qti.browser.execute_script("restoreOriginalMethods();")
            # print(1/0)
    except Exception as e:
        print(e)
        pass
    qti.Close()

def 微信读书MainV2(begin_url, book_name=None):
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    该函数只能获取所有已经绘制在canvas中的文本内容，
    以及穿插在文本中的上传的图片
    除了上面的功能还具有：
    获得已经渲染在网页上切实乱序的网站的内容
    '''
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                       virtual_chrome=True, # 使用虚拟浏览器
                       debug=False)
    # qti.OpenChrome()
    qti.OpenBaseChrome(virtual_browser=True)
    # 最大化浏览器窗口
    qti.browser.maximize_window()

    if book_name is None:
        time_str = time.strftime('%Y_%m_%d',time.localtime(time.time()))
        book_name = f"微信阅读_{time_str}"

    save_file = rf"{BIC['base_path']}\url_list_{book_name}.txt"
    save_book = rf"{BIC['base_path']}\{book_name}.txt"

    try:
        # 中途异常退出
        with codecs.open(save_file, "r", "utf-8") as fr:
            url_lines = fr.readlines()
    except:
        # 首次执行
        url_lines = []

    qti.browser.get(begin_url)
    sleep(5)
    # 使用包含类名 isHorizontalReader 的 XPath 定位元素
    # 类中包含 isHorizontalReader 表示处于双页阅读；isNormalReader 表示处于滚动阅读
    read_model_handle = qti.GetHandle(".//self::button[contains(@class, 'isHorizontalReader')]")
    if read_model_handle is not None:
        read_model_handle.click()
    # # 如果要获得目录的标题需要先展开目录才行
    # qti.Click(".//self::button[@class='readerControls_item catalog']")
    # sleep(1)
    # 获取目录数量. 包含匹配的方式获取
    begin_index = 0
    if url_lines == []:
        GetwereadQQBookAllUrlV3(qti, begin_url, save_file, begin_index=begin_index)
    else:
        contents_handles = qti.GetHandles(".//self::li[contains(@class, 'readerCatalog_list_item')]")
        # for index, content in enumerate(contents_handles):
        #     # 如果没有登录账号，那么只能获取免费的目录
        #     print(f"{index}; {content.text}") #content.text 需要先展开书的目录
        if contents_handles is not None:
            # 获取书所有的章节url
            last_url = url_lines[-1].split(";")[-1].strip()
            begin_index = len(url_lines)
        # if begin_index != len(contents_handles):
        #     GetwereadQQBookAllUrlV3(qti, last_url, save_file, begin_index=begin_index)

    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法， 在调用时将文本内容及其位置、样式等信息存储到 capturedText 数组中，然后调用原始的 fillText 方法。
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline,
            fontSize: this.font.split('px')[0], // 字体大小
            lineHeight: this.font.split('px')[0] * 1.2, // 行高
            textWidth: this.measureText(text).width, // 文本宽度
            textLines: text.split('\\n').length // 文本行数
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法，功能与 fillText 方法类似，将文本内容及其相关信息存储到 capturedText 数组中，然后调用原始的 strokeText 方法。
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    debugger
    console.log(capturedText)
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let contents_arr = [];
    let lastY = null;
    let last_style = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 40) {
            result += '\\n'; // 插入换行符
            //result += "YYY:"+lastY+'\\n'; // 插入换行符
            contents_arr.push({
                "Y":lastY,
                "content":result,
                "item":last_style
            })
            result = ""
        }
        result += item.text + '';
        lastY = item.y;
        last_style = item
    });
    if (result !== "" && last_style !== null){
        contents_arr.push({
            "Y":lastY,
            "content":result,
            "item":last_style
        })
    }
    

    // return result.trim();
    return contents_arr
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''

#     script = '''
# // 存储捕获的文本内容和矩形框信息
# let capturedText = [];
# let capturedRects = [];

# // 保存原始的 fillText, strokeText 和 rect 方法
# const originalFillText = CanvasRenderingContext2D.prototype.fillText;
# const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
# const originalRect = CanvasRenderingContext2D.prototype.rect;

# // 重写 fillText 方法
# CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
#     capturedText.push({
#         text: text,
#         x: x,
#         y: y,
#         maxWidth: maxWidth,
#         type: 'fill',
#         style: {
#             font: this.font,
#             fillStyle: this.fillStyle,
#             textAlign: this.textAlign,
#             textBaseline: this.textBaseline,
#             fontSize: this.font.split('px')[0], // 字体大小
#             lineHeight: this.font.split('px')[0] * 1.2, // 行高
#             textWidth: this.measureText(text).width, // 文本宽度
#             textLines: text.split('\\n').length // 文本行数
#         }
#     });
#     return originalFillText.apply(this, arguments);
# };

# // 重写 strokeText 方法
# CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
#     capturedText.push({
#         text: text,
#         x: x,
#         y: y,
#         maxWidth: maxWidth,
#         type: 'stroke',
#         style: {
#             font: this.font,
#             strokeStyle: this.strokeStyle,
#             textAlign: this.textAlign,
#             textBaseline: this.textBaseline
#         }
#     });
#     return originalStrokeText.apply(this, arguments);
# };

# // 重写 rect 方法
# CanvasRenderingContext2D.prototype.rect = function(x, y, width, height) {
#     capturedRects.push({
#         x: x,
#         y: y,
#         width: width,
#         height: height,
#         type: 'rect',
#         isRounded: false, // 默认为非圆角矩形
#         style: {
#             strokeStyle: this.strokeStyle,
#             fillStyle: this.fillStyle,
#             lineWidth: this.lineWidth
#         }
#     });
#     return originalRect.apply(this, arguments);
# };

# // 获取捕获的文本内容和矩形框信息
# window.getCapturedTextAndRects = function() {
#     const sortedText = capturedText.sort((a, b) => {
#         if (Math.abs(a.y - b.y) > 10) {
#             return a.y - b.y;
#         }
#         return a.x - b.x;
#     });

#     let result = '';
#     let contents_arr = [];
#     let lastY = null;
#     let last_style = null;
#     sortedText.forEach(item => {
#         if (lastY !== null && Math.abs(item.y - lastY) > 40) {
#             result += '\\n'; // 插入换行符
#             contents_arr.push({
#                 "Y": lastY,
#                 "content": result,
#                 "item": last_style
#             });
#             result = "";
#         }
#         result += item.text + '';
#         lastY = item.y;
#         last_style = item;
#     });
#     if (result !== "" && last_style !== null) {
#         contents_arr.push({
#             "Y": lastY,
#             "content": result,
#             "item": last_style
#         });
#     }

#     return {
#         text: contents_arr,
#         rects: capturedRects
#     };
# };

# // 清除已捕获的文本内容和矩形框信息
# window.clearCapturedTextAndRects = function() {
#     capturedText = [];
#     capturedRects = [];
# };

# // 恢复原始方法
# window.restoreOriginalMethods = function() {
#     CanvasRenderingContext2D.prototype.fillText = originalFillText;
#     CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
#     CanvasRenderingContext2D.prototype.rect = originalRect;
# };
# '''

    img_script='''
// function getAllImgs(){
window.getAllImgs = function(){
    // 获取 <img> 元素
    const imgElement = document.getElementsByTagName('img');

    let imgs = []
    for(let handle of imgElement){
        const classes = handle.className;
        // width60 wr_absolute wr_readerImage_opacity
        // width80 wr_absolute wr_readerImage_opacity
        if (classes.indexOf("wr_absolute wr_readerImage_opacity") ===-1)continue
        console.log("className",classes)
        // 获取坐标和长宽信息
        const rect = handle.getBoundingClientRect();
        const imgWidth = rect.width;
        const imgHeight = rect.height;
        const imgTop = rect.top;
        const imgLeft = rect.left;

        // 输出信息
        console.log(`Width: ${imgWidth}, Height: ${imgHeight}`);
        console.log(`Top: ${imgTop}, Left: ${imgLeft}`);

        // 获取样式信息
        const style = handle.style;
        

        // 解析坐标和尺寸
        const transform = style.transform;
        const width = style.width;
        const height = style.height;

        // 提取坐标值
        const translateX = transform.match(/translate\((\d+)px, (\d+)px\)/)[1];
        const translateY = transform.match(/translate\((\d+)px, (\d+)px\)/)[2];

        console.log(`X坐标: ${translateX}px`);
        console.log(`Y坐标: ${translateY}px`);
        console.log(`宽度: ${width}`);
        console.log(`高度: ${height}`);
        imgs.push({
        "src":handle.src,
        "X坐标":parseInt(translateX),
        "Y坐标":parseFloat(translateY),
        "宽度":width,
        "高度":height,
        "className":classes,
        })
    }
    return imgs
}
'''

    # 获得已经存储的book的最后一个章节位置
    try:
        with codecs.open(save_book, "r", "utf-8") as fr:
            book_lines = fr.readlines()
        begin = int(book_lines[-1].split(r"\t")[0].strip())
    except:
        begin = 0

    # 再读一次完整的url——list
    with codecs.open(save_file, "r", "utf-8") as fr:
        url_lines = fr.readlines()
    book_content = []
    try:
        for index in range(begin, len(url_lines)):
        # for index, line in enumerate(url_lines):
            # 注入js之后需要更换页面内容才可以使用 getCapturedText 获得最新的内容，因此需要向上翻一页之后再点击下一章才可以获得当前章节内容
            # 所以url才需要向下面一样向上取一个
            # if index == 0:  url = begin_url
            if index == 0:  url = url_lines[index+1].split(";")[-1].strip()
            else:           url =  url_lines[index].split(";")[-1].strip()
            # 测试使用，这是运行需要关闭 begin
            url = "https://weread.qq.com/web/reader/cf132e10813ab92e9g018088kc81322c012c81e728d9d180"
            # 测试使用，这是运行需要关闭 end 
            qti.browser.get(url)
            sleep(5)
            # 注入js
            qti.browser.execute_script(script)
            if index == 0:
                # 首页需要使用点击上一章才能获取完整
                next_handle = qti.GetHandle(xpath=".//self::button[@class='readerHeaderButton']")
            else:
                # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
                next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
            if next_handle is None:
                break
            next_handle.click()
            sleep(5)
            # 获取内容
            qti.browser.execute_script(img_script) #注入获取图片的脚本
            canvas_info = qti.browser.execute_script("return getCapturedText();")
            img_dict_list = qti.browser.execute_script("return getAllImgs();")
            new_canvas_info = {data_dict["Y"]:data_dict["content"] for data_dict in canvas_info}
            new_img_dict = {int(img_dict['Y坐标']):img_dict for img_dict in img_dict_list}
            combined_sorted_keys = sorted(list(new_canvas_info.keys()) + list(new_img_dict.keys()))
            new_content = []
            for key in combined_sorted_keys:
                if key in list(new_canvas_info.keys()):
                    new_content.append(new_canvas_info[key])
                else:
                    # new_content.append(f"{str(new_img_dict[key])}\n")
                    pass
            canvas_info = "".join(new_content)
            print(canvas_info)
            book_content.append(canvas_info)
            with codecs.open(save_book, "a+", "utf-8") as fa:
                fa.write(f"{canvas_info}\n{index+1}\t\n")
            # 清除捕获的文本内容
            qti.browser.execute_script("clearCapturedText();")

            # 恢复原始方法
            qti.browser.execute_script("restoreOriginalMethods();")
            # print(1/0)
    except Exception as e:
        print(e)
        pass
    qti.Close()

def 微信读书_一章Main(begin_url=None, url_list=None):
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    
    '''
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                       debug=False)
    qti.OpenChrome()

    if begin_url is None:
        begin_url = "https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180"
    book_name = "明朝那些事"
    save_file = rf"{BIC['base_path']}\url_list_{book_name}.txt"
    save_book = rf"{BIC['base_path']}\{book_name}.txt"

    # 获取书所有的章节url
    # GetwereadQQBookAllUrl(qti, begin_url, save_file)

    with codecs.open(save_file, "r", "utf-8") as fr:
        url_lines = fr.readlines()
    
    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let lastY = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 10) {
            result += '\\n'; // 插入换行符
        }
        result += item.text + ' ';
        lastY = item.y;
    });

    return result.trim();
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''
    
    # 获得已经存储的book的最后一个章节位置
    try:
        with codecs.open(save_book, "r", "utf-8") as fr:
            book_lines = fr.readlines()
        begin = int(book_lines[-1].split(r"\t")[0].strip())
    except:
        begin = 0
    book_content = []
    try:
        for index in range(begin, len(url_lines)):
        # for index, line in enumerate(url_lines):
            # 注入js之后需要更换页面内容才可以使用 getCapturedText 获得最新的内容，因此需要向上翻一页之后再点击下一章才可以获得当前章节内容
            # 所以url才需要向下面一样向上取一个
            if index == 0:  url = begin_url
            else:           url =  url_lines[index-1].strip()
            qti.browser.get(url)
            sleep(2)
            # 注入js
            qti.browser.execute_script(script)
            # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
            next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
            if next_handle is None:
                break
            next_handle.click()
            sleep(3)
            # 获取内容
            canvas_info = qti.browser.execute_script("return getCapturedText();")
            canvas_info ="".join(canvas_info.split(" ")) #去除内部多余的空格
            book_content.append(rf"{index+1}\t{canvas_info}@@@***@@@***")
            # 清除捕获的文本内容
            qti.browser.execute_script("clearCapturedText();")

            # 恢复原始方法
            qti.browser.execute_script("restoreOriginalMethods();")
            # print(1/0)
    except:
        with codecs.open(save_book, "a+", "utf-8") as fa:
            fa.write("\n".join(book_content))
            fa.write("\n")


    qti.Close()

import re
def is_chinese_punctuation(char):
    # 中文标点符号的Unicode范围
    chinese_punctuation = r'[\u3000-\u303F\uFF00-\uFFEF]'
    return re.match(chinese_punctuation, char) is not None

def check_last_char_is_chinese_punctuation(s):
    if not s:
        return False
    return is_chinese_punctuation(s[-1])

def 测试获取文本和图片的信息():
    '''
    @Time    :   2025/01/15 16:54:26
    @功能    :   None
    '''
    qti = selenium_qti(browser=None,
                       url="https://weread.qq.com/web/reader/77e326b072922e9177e6cb1kc7432af0210c74d97b01b1c",
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                       debug=False)
    qti.OpenChrome()
    sleep(2)
    
    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法， 在调用时将文本内容及其位置、样式等信息存储到 capturedText 数组中，然后调用原始的 fillText 方法。
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline,
            fontSize: this.font.split('px')[0], // 字体大小
            lineHeight: this.font.split('px')[0] * 1.2, // 行高
            textWidth: this.measureText(text).width, // 文本宽度
            textLines: text.split('\\n').length // 文本行数
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法，功能与 fillText 方法类似，将文本内容及其相关信息存储到 capturedText 数组中，然后调用原始的 strokeText 方法。
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    debugger
    console.log(capturedText)
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let contents_arr = [];
    let lastY = null;
    let last_style = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 40) {
            result += '\\n'; // 插入换行符
            //result += "YYY:"+lastY+'\\n'; // 插入换行符
            contents_arr.push({
                "Y":lastY,
                "content":result,
                "item":last_style
            })
            result = ""
        }
        result += item.text + '';
        lastY = item.y;
        last_style = item
    });
    contents_arr.push({
        "Y":lastY,
        "content":result,
        "item":last_style
    })

    // return result.trim();
    return contents_arr
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''

    img_script='''
// function getAllImgs(){
window.getAllImgs = function(){
    // 获取 <img> 元素
    const imgElement = document.getElementsByTagName('img');

    let imgs = []
    for(let handle of imgElement){
        const classes = handle.className;
        if (classes.indexOf("width80 wr_absolute wr_readerImage_opacity") ===-1)continue
        console.log("className",classes)
        // 获取坐标和长宽信息
        const rect = handle.getBoundingClientRect();
        const imgWidth = rect.width;
        const imgHeight = rect.height;
        const imgTop = rect.top;
        const imgLeft = rect.left;

        // 输出信息
        console.log(`Width: ${imgWidth}, Height: ${imgHeight}`);
        console.log(`Top: ${imgTop}, Left: ${imgLeft}`);

        // 获取样式信息
        const style = handle.style;
        

        // 解析坐标和尺寸
        const transform = style.transform;
        const width = style.width;
        const height = style.height;

        // 提取坐标值
        const translateX = transform.match(/translate\((\d+)px, (\d+)px\)/)[1];
        const translateY = transform.match(/translate\((\d+)px, (\d+)px\)/)[2];

        console.log(`X坐标: ${translateX}px`);
        console.log(`Y坐标: ${translateY}px`);
        console.log(`宽度: ${width}`);
        console.log(`高度: ${height}`);
        imgs.push({
        "src":handle.src,
        "X坐标":parseInt(translateX),
        "Y坐标":parseFloat(translateY),
        "宽度":width,
        "高度":height,
        "className":classes,
        })
    }
    return imgs
}
'''

    sleep(2)
    # 注入js
    qti.browser.execute_script(script)
    qti.browser.execute_script(img_script)
    # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
    sleep(3)
    # 获取内容
    canvas_info = qti.browser.execute_script("return getCapturedText();")
    img_dict_list = qti.browser.execute_script("return getAllImgs();")
    new_canvas_info = {data_dict["Y"]:data_dict["content"] for data_dict in canvas_info}
    new_img_dict = {int(img_dict['Y坐标']):img_dict for img_dict in img_dict_list}
    combined_sorted_keys = sorted(list(new_canvas_info.keys()) + list(new_img_dict.keys()))
    new_content = []
    for key in combined_sorted_keys:
        if key in list(new_canvas_info.keys()):
            new_content.append(new_canvas_info[key])
        else:
            new_content.append(f"{str(new_img_dict[key])}\n")
    print(canvas_info)
    # 清除捕获的文本内容
    qti.browser.execute_script("clearCapturedText();")
    # 恢复原始方法
    qti.browser.execute_script("restoreOriginalMethods();")
    # print(1/0)
    qti.Close()
    pass
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.utils import ImageReader
# from reportlab.lib.colors import HexColor

# # 创建PDF文件
# c = canvas.Canvas(r'C:\Dropbox\YAN\D\2025\zhiguol\WeChatRead\output.pdf', pagesize=letter)

# # 注册支持中文的字体
# pdfmetrics.registerFont(TTFont('SimSun', r'C:\Windows\Fonts\simsunb.ttf'))

# # 设置字体
# c.setFont('SimSun', 12)

# # 添加灰色背景
# c.setFillColor(HexColor("#D3D3D3"))  # 灰色
# c.rect(0, 0, letter[0], letter[1], fill=1)

# # 设置字体颜色为黑色
# c.setFillColor(HexColor("#000000"))

# # 添加文本
# text = '''
# 这是一些文本数据。
# Using cached chardet-5.2.0-py3-none-any.whl.metadata (3.4 kB)
# Using cached reportlab-4.2.5-py3-none-any.whl (1.9 MB)
# Using cached chardet-5.2.0-py3-none-any.whl (199 kB)
# Installing collected packages: chardet, reportlab
# '''

# # 使用TextObject处理换行
# text_object = c.beginText(100, 750)
# text_object.setFont('SimSun', 12)
# for line in text.split('\n'):
#     text_object.textLine(line)
# c.drawText(text_object)

# # 添加图片
# image = ImageReader(r'C:\Dropbox\YAN\D\2025\zhiguol\WeChatRead\test.jpg')
# c.drawImage(image, 150, 600, width=200, height=200)
# # c.drawImage(image, 150, 500)

# # 保存PDF文件
# c.save()


# from docx import Document
# from docx.shared import Inches

# # 创建一个新的Word文档
# doc = Document()

# # 添加标题
# doc.add_heading('Document Title', 0)

# # 添加段落
# doc.add_paragraph('这是一个段落。')

# # 添加带格式的段落
# doc.add_paragraph(
#     '这是一个带有加粗和斜体的段落。'
#     ' 你可以使用不同的格式来丰富内容。',
#     style='Intense Quote'
# )

# # 插入图片
# doc.add_picture(r'C:\Dropbox\YAN\D\2025\zhiguol\WeChatRead\test.jpg', width=Inches(4.0))
# # 添加带格式的段落
# doc.add_paragraph(
#     '这是一个带有加粗和斜体的段落。'
#     ' 你可以使用不同的格式来丰富内容。',
#     style='Intense Quote'
# )
# # 保存文档
# doc.save(r'C:\Dropbox\YAN\D\2025\zhiguol\WeChatRead\document.docx')

# # 定义Markdown内容
# markdown_content = '''
# # 示例Markdown文件

# 这是一个示例Markdown文件，其中包含文本和图片。

# !示例图片
# '''

# # 将Markdown内容写入文件
# with open(r'C:\Dropbox\YAN\D\2025\zhiguol\WeChatRead\example.md', 'w', encoding='utf-8') as file:
#     file.write(markdown_content)
#     file.write(r'C:\Dropbox\YAN\D\2025\zhiguol\WeChatRead\test.jpg')

def is_scroll_to_bottom(qti):
    """
    判断滚动条是否已经滚动到底部。
    
    :param driver: Selenium WebDriver实例
    :return: True表示滚动到底部，False表示未到底部
    """
    # 执行JavaScript代码获取页面高度和滚动位置
    scroll_height = qti.browser.execute_script("return document.body.scrollHeight;")
    window_height = qti.browser.execute_script("return window.innerHeight;")
    scroll_position = qti.browser.execute_script("return window.scrollY;")
    # 判断是否滚动到底部
    return scroll_height <= window_height + scroll_position

def 微信读书MainV2测试获取已经被渲染到网页的文本(begin_url, book_name=None):
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    该函数只能获取所有已经绘制在canvas中的文本内容，
    以及穿插在文本中的上传的图片
    除了上面的功能还具有：
    获得已经渲染在网页上切实乱序的网站的内容
    '''
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                       virtual_chrome=True, # 使用虚拟浏览器
                       debug=False)
    # qti.OpenChrome()
    qti.OpenBaseChrome(virtual_browser=True)
    qti.browser.get(begin_url)
    # 最大化浏览器窗口
    qti.browser.maximize_window()

    # 使用包含类名 isHorizontalReader 的 XPath 定位元素
    # 类中包含 isHorizontalReader 表示处于双页阅读；isNormalReader 表示处于滚动阅读
    read_model_handle = qti.GetHandle(".//self::button[contains(@class, 'isHorizontalReader')]")
    if read_model_handle is not None:
        read_model_handle.click()
    # # 如果要获得目录的标题需要先展开目录才行
    # qti.Click(".//self::button[@class='readerControls_item catalog']")
    # sleep(1)
    # 获取目录数量. 包含匹配的方式获取
    
    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法， 在调用时将文本内容及其位置、样式等信息存储到 capturedText 数组中，然后调用原始的 fillText 方法。
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline,
            fontSize: this.font.split('px')[0], // 字体大小
            lineHeight: this.font.split('px')[0] * 1.2, // 行高
            textWidth: this.measureText(text).width, // 文本宽度
            textLines: text.split('\\n').length // 文本行数
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法，功能与 fillText 方法类似，将文本内容及其相关信息存储到 capturedText 数组中，然后调用原始的 strokeText 方法。
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    debugger
    console.log(capturedText)
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let contents_arr = [];
    let lastY = null;
    let last_style = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 40) {
            result += '\\n'; // 插入换行符
            //result += "YYY:"+lastY+'\\n'; // 插入换行符
            contents_arr.push({
                "Y":lastY,
                "content":result,
                "item":last_style
            })
            result = ""
        }
        result += item.text + '';
        lastY = item.y;
        last_style = item
    });
    if (result !== "" && last_style !== null){
        contents_arr.push({
            "Y":lastY,
            "content":result,
            "item":last_style
        })
    }
    

    // return result.trim();
    return contents_arr
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''


    book_content = []
    try:
        # 测试使用，这是运行需要关闭 begin
        # url = "https://weread.qq.com/web/reader/cf132e10813ab92e9g018088ka87322c014a87ff679a21ea"
        # # 测试使用，这是运行需要关闭 end 
        # qti.browser.get(url)
        # sleep(5)
        # 注入js
        qti.browser.execute_script(script)
        # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        next_handle.click()
        sleep(5)
        # 获取内容
        canvas_info = qti.browser.execute_script("return getCapturedText();")
        html_content = 循环获得已经渲染到网页的动态内容(qti)
        print(canvas_info)
        book_content.append(f"{canvas_info}\n{html_content}")
        # 清除捕获的文本内容
        qti.browser.execute_script("clearCapturedText();")

        # 恢复原始方法
        qti.browser.execute_script("restoreOriginalMethods();")
        # print(1/0)
    except Exception as e:
        print(e)
        pass
    qti.Close()

from bs4 import BeautifulSoup
from 通过位置渲染的文本 import html_innerHtml
import re

def 循环获得已经渲染到网页的动态内容(qti):
    '''
    @Time    :   2025/01/21 17:38:11
    @功能    :   循环获得已经渲染到网页的所有文本
    注意这里的文本是随着滚动条而动态出现和动态消失的，一次滚动条每次不能滚动条太多
    '''
    context_html_list = []
    while 1:
        if is_scroll_to_bottom(qti):
            print("滚动条已经滚动到底部")
            break
        qti.ScrollBar_相对位置(200) #向下滚动100个单位
        handles = qti.GetHandles(".//self::div[@class='passage-wrapper']//div[@class='passage-content']")
        for index, handle in enumerate(handles):
            if index == 0: continue
            content_html = handle.get_attribute("innerHTML")
            if content_html not in context_html_list:
                context_html_list.append(content_html)

        # if len(handles) != 1:
        #     print(handles[1].get_attribute("innerHTML"))
        print(len(handles))
        time.sleep(1)
        pass
    context_list = []
    for index, content_html in enumerate(context_html_list):
        content = [data_dict["content"] for data_dict in 重组文本(content_html)]
        context_list.append("\n".join(content))
    html_content = "\n".join(context_list)
    return html_content

def 重组文本(html_body):
    '''
    @Time    :   2025/01/21 16:34:02
    @功能    :   None
    '''
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html_body, 'html.parser')
    # 获取所有具有data-wr-role属性的span元素
    spans = soup.find_all('span', {'data-wr-role': 'text'})

    # 遍历每个span元素并获取其属性和文本内容
    # 获取y轴数据
    text_dict = {}
    for span in spans:
        data_wr_id = span.get('data-wr-id')
        data_wr_role = span.get('data-wr-role')
        class_name = span.get('class')
        style = span.get('style')
        text_content = span.text
        # # 打印属性和文本内容
        # print('data-wr-id:', data_wr_id)
        # print('data-wr-role:', data_wr_role)
        # print('class:', class_name)
        # print('style:', style)
        # print('textContent:', text_content)
        # print('-------------------------')
        pattern = r"translate\((\d+)px,\s*(\d+)px\)"
        match = re.search(pattern, style)
        if match:
            x_value = int(match.group(1))  # 提取第一个数值
            y_value = int(match.group(2))  # 提取第二个数值
            print(f"X值: {x_value}")
            print(f"Y值: {y_value}")
            if y_value in list(text_dict.keys()):
                text_dict[y_value].append({
                    "x":x_value,
                    "text":span.text
                })
            else:
                text_dict[y_value] = [{
                    "x":x_value,
                    "text":span.text
                }]
        else:
            continue

    # 排序y轴数据
    new_y_list = sorted(list(text_dict.keys()))
    new_text_dict = {}
    for index, key in enumerate(new_y_list):
        new_text_dict[key] = text_dict[key]

    # 排序x轴数据
    for key, data_dict_list in new_text_dict.items():
        sorted_data = sorted(data_dict_list, key=lambda item: item['x'])
        content = [data_dict["text"] for data_dict in sorted_data]
        new_text_dict[key] = {
            "x":sorted_data[0]["x"],
            "content":"".join(content)
        }

    # 根据y轴差值是否超过40来判定是否属于一行
    # 初始化结果列表
    result = []
    # 遍历排序后的键
    keys = list(new_text_dict.keys())
    for i in range(len(keys)):
        current_key = keys[i]
        current_text = new_text_dict[current_key]
        # 如果是第一个键，直接添加到结果列表
        if i == 0:
            result.append(current_text)
        else:
            previous_key = keys[i - 1]
            # 如果当前键和前一个键的差值不超过40，合并文本
            if current_key - previous_key <= 40:
                result[-1]["content"] += current_text["content"]  # 合并到上一个文本
            else:
                result.append(current_text)  # 新增一个文本
    # 输出结果
    # 可以根据X轴的坐标起始位置判断这段文字所有在的行初始位置
    for idx, text in enumerate(result):
        print(f"段落 {idx + 1}: {text['content']}")
    return result

if __name__=='__main__':
    # MainDemo()
    # 微信读书Main("https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180")
    # 微信读书Main("https://weread.qq.com/web/reader/77e326b072922e9177e6cb1kecc32f3013eccbc87e4b62e", book_name="对赌_test")
    # 微信读书Main("https://weread.qq.com/web/reader/77e326b072922e9177e6cb1kc81322c012c81e728d9d180", book_name="对赌_test11")
    # 微信读书Main("https://weread.qq.com/web/reader/214327005b6b3621437a4f5k16732dc0161679091c5aeb1", book_name="华尔街英语创始人的幸福成功学")
    微信读书Main("https://weread.qq.com/web/reader/cf132e10813ab92e9g018088ka87322c014a87ff679a21ea", book_name="思辨力35讲：像辩手一样思考")
    # 微信读书MainV2测试获取已经被渲染到网页的文本("https://weread.qq.com/web/reader/cf132e10813ab92e9g018088ka87322c014a87ff679a21ea", book_name="思辨力35讲：像辩手一样思考")
    # 重组文本(html_innerHtml)
    # 测试获取文本和图片的信息()



