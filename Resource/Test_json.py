def appendData_to_flex(new_digest):
    data = {
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "bubble",
    "header": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "text",
          "text": new_digest,
          "size": "sm",
          "weight": "bold",
          "color": "#AAAAAA"
        }
      ]
    },
    "hero": {
      "type": "image",
      "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_4_news.png",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "label": "Action",
        "uri": "https://linecorp.com/"
      }
    },
    "body": {
      "type": "box",
      "layout": "horizontal",
      "spacing": "md",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "flex": 1,
          "contents": [
            {
              "type": "image",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/02_1_news_thumbnail_1.png",
              "gravity": "bottom",
              "size": "sm",
              "aspectRatio": "4:3",
              "aspectMode": "cover"
            },
            {
              "type": "image",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/02_1_news_thumbnail_2.png",
              "margin": "md",
              "size": "sm",
              "aspectRatio": "4:3",
              "aspectMode": "cover"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "flex": 2,
          "contents": [
            {
              "type": "text",
              "text": "7 Things to Know for Today",
              "flex": 1,
              "size": "xs",
              "gravity": "top"
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "Hay fever goes wild",
              "flex": 2,
              "size": "xs",
              "gravity": "center"
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "LINE Pay Begins Barcode Payment Service",
              "flex": 2,
              "size": "xs",
              "gravity": "center"
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "LINE Adds LINE Wallet",
              "flex": 1,
              "size": "xs",
              "gravity": "bottom"
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "More",
            "uri": "https://linecorp.com"
          }
        }
      ]
    }
  }
}
    return data