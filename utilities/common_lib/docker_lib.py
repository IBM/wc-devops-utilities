import requests
import re

def main():
  regExpress="v1-[0-9]{8}-[0-9]{4}.*"
  print("call harbor API to get repository tag list")
  url="http://9.110.182.141/api/repositories/commerce/ts-app/tags"
  ts_r = requests.get(url=url,verify=False)
  tags = ts_r.json()
  tags = [tag for tag in tags if re.match(regExpress,tag)]
  tags.reverse()

  print(tags)


if __name__ == '__main__':
    main()