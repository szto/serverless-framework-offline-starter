import requests
import json


def date_converter(date_string):
    """
    날짜변환함수
    19840526 -> 1884-05-26
    """
    return date_string[:4] + "-" + date_string[4:6] + "-" + date_string[6:8]


def get_lotte_abroad_travel(serializer):

    INSURANCE_COMPANY = "LO"  # 롯대손해보험 - 해외여행자보험

    insurance_request = serializer.get("request_id", None)
    birthday = serializer.get("birthday", None)
    gender = serializer.get("gender", None)
    start_date = serializer.get("start_date", None)
    end_date = serializer.get("end_date", None)
    start_date_converter = date_converter(start_date)
    end_date_converter = date_converter(end_date)

    birthday_short = birthday[2:]
    gender_convert = "1" if gender == "M" else "2"

    with requests.session() as s:
        s.get("https://m.lottehowmuch.com")
        s.get("https://m.lottehowmuch.com/CChannelSvl#!/web/C/M/L/cml000_ot")

        # 표준플랜 - 해외
        data = [
            ("tc", "dfi.c.c.l.cmd.Ccl300Cmd"),
            ("rtnUri", "/web/C/C/K/returnJsonData.jsp"),
            ("cmd", ""),
            ("task", ""),
            ("pageTypeCd", "getRandingCalc"),
            ("Grpkind", "01"),
            ("minor", "false"),
            ("ThreeMonthOver", "N"),
            ("startDate", start_date_converter),
            ("endDate", end_date_converter),
            ("planType", "OB"),
            ("dateGap", ""),
            ("msgTxt", "3655"),
            ("sex", gender_convert),
            ("sexF", "1"),
            ("Isex1", "2"),
            ("Isex2", "1"),
            ("Isex3", "1"),
            ("Isex4", "1"),
            ("Isex5", "1"),
            ("Isex6", "1"),
            ("eventPage", "NIDIC900003001"),
            ("prnoA", birthday_short),
            ("partner", "1"),
            ("children", "0"),
            ("damboJoin1", "1"),
            ("damboJoin2", "1"),
            ("damboJoin3", "1"),
            ("damboJoin4", "1"),
            ("damboJoin5", "1"),
            ("damboJoin6", "1"),
            ("damboJoin7", "1"),
            ("damboJoin8", "1"),
            ("damboJoin9", "1"),
            ("damboJoin10", "1"),
            ("damboJoin11", "1"),
            ("damboJoin12", "1"),
            ("damboJoin13", "1"),
            ("damboJoin14", "1"),
            ("dpremJoin14", "1"),
            ("dpremJoin15", "1"),
            ("dpremJoin16", "1"),
            ("K_BOJCODE", "1448"),
            ("sexP", gender_convert),
            ("mobileYN", "Y"),
            ("tourPurposeCd", "1"),
            ("tourPurposeCd", "1"),
            ("prnoA_family", ""),
            ("IsdrnoF", ""),
            ("chksex", "on"),
            ("prnoAtext", birthday),
            ("check-agr123", "on"),
        ]

        response = s.post("https://m.lottehowmuch.com/CChannelSvl", data=data)
        res_json_mid = response.json()
        face_amount_mid = res_json_mid["payload"]["fnlCcPrm"]

        # 실속플랜 - 해외
        data = {
            "startDate": start_date_converter,
            "endDate": end_date_converter,
            "prnoA": birthday_short,
            "tc": "dfi.c.c.l.cmd.Ccl300Cmd",
            "rtnUri": "/web/C/C/K/returnJsonData.jsp",
            "cmd": "",
            "task": "",
            "pageTypeCd": "getCalc",
            "planType": "OA",
            "Grpkind": "01",
            "minor": "false",
            "K_BOJCODE": "1448",
            "KChungno": "",
            "Twprem": "",
            "planTypeTxt": "\uD45C\uC900\uD50C\uB79C",
            "damboJoin0": "0",
            "damboJoin1": "1",
            "damboJoin2": "1",
            "damboJoin3": "1",
            "damboJoin4": "1",
            "damboJoin5": "1",
            "damboJoin6": "1",
            "damboJoin7": "1",
            "damboJoin8": "1",
            "damboJoin9": "1",
            "damboJoin10": "1",
            "damboJoin11": "1",
            "damboJoin12": "1",
            "damboJoin13": "1",
            "damboJoin14": "0",
            "dpremJoin14": "1",
            "dpremJoin15": "1",
            "dpremJoin16": "1",
            "ThreeMonthOver": "N",
            "eventPage": "NIDIC900003001",
            "mobileYN": "Y",
            "longRending": "null",
            "sms_RCustnm": "",
            "sms_regno1": "",
            "sms_regno2": "",
            "RHpNo2": "",
            "RHpNo3": "",
            "certiNum": "",
            "RCustnm": "",
            "regno1": "",
            "regno2": "",
            "card_RCustnm": "",
            "card_regno1": "",
            "card_regno2": "",
            "usr_Card01": "",
            "usr_Card02": "",
            "usr_Card03": "",
            "usr_Card04": "",
            "card_PW": "",
            "email01": "",
            "email02": "",
            "email03": "1",
            "check-agr1231": "1",
            # 'transkeyUuid': 'c4afdf4a814c61dcff48b4b70349000529b6d4db',
            "transkey_regno2": "",
            "transkey_HM_regno2": "",
            "transkey_card_regno2": "",
            "transkey_HM_card_regno2": "",
            "transkey_usr_Card02": "",
            "transkey_HM_usr_Card02": "",
            "transkey_usr_Card03": "",
            "transkey_HM_usr_Card03": "",
            "transkey_card_PW": "",
            "transkey_HM_card_PW": "",
        }

        response = s.post("https://m.lottehowmuch.com/CChannelSvl", data=data)
        res_json_low = response.json()
        face_amount_low = res_json_low["payload"]["fnlCcPrm"]

        # 고급플랜 - 해외
        data = {
            "tc": "dfi.c.c.l.cmd.Ccl300Cmd",
            "rtnUri": "/web/C/C/K/returnJsonData.jsp",
            "cmd": "",
            "task": "",
            "pageTypeCd": "getCalc",
            "planType": "OC",
            "Grpkind": "01",
            "minor": "false",
            "K_BOJCODE": "1448",
            "KChungno": "",
            "startDate": start_date_converter,
            "endDate": end_date_converter,
            "Twprem": "",
            "prnoA": birthday_short,
            "planTypeTxt": "\uC2E4\uC18D\uD50C\uB79C",
            "damboJoin0": "0",
            "damboJoin1": "1",
            "damboJoin2": "1",
            "damboJoin3": "1",
            "damboJoin4": "1",
            "damboJoin5": "1",
            "damboJoin6": "1",
            "damboJoin7": "1",
            "damboJoin8": "1",
            "damboJoin9": "1",
            "damboJoin10": "1",
            "damboJoin11": "1",
            "damboJoin12": "1",
            "damboJoin13": "1",
            "damboJoin14": "1",
            "dpremJoin14": "1",
            "dpremJoin15": "1",
            "dpremJoin16": "1",
            "ThreeMonthOver": "N",
            "eventPage": "NIDIC900003001",
            "mobileYN": "Y",
            "longRending": "null",
            "sms_RCustnm": "",
            "sms_regno1": "",
            "sms_regno2": "",
            "RHpNo2": "",
            "RHpNo3": "",
            "certiNum": "",
            "RCustnm": "",
            "regno1": "",
            "regno2": "",
            "card_RCustnm": "",
            "card_regno1": "",
            "card_regno2": "",
            "usr_Card01": "",
            "usr_Card02": "",
            "usr_Card03": "",
            "usr_Card04": "",
            "card_PW": "",
            "email01": "",
            "email02": "",
            "email03": "1",
            "check-agr1233": "3",
            # 'transkeyUuid': 'c4afdf4a814c61dcff48b4b70349000529b6d4db',
            "transkey_regno2": "",
            "transkey_HM_regno2": "",
            "transkey_card_regno2": "",
            "transkey_HM_card_regno2": "",
            "transkey_usr_Card02": "",
            "transkey_HM_usr_Card02": "",
            "transkey_usr_Card03": "",
            "transkey_HM_usr_Card03": "",
            "transkey_card_PW": "",
            "transkey_HM_card_PW": "",
        }
        response = s.post("https://m.lottehowmuch.com/CChannelSvl", data=data)
        res_json_high = response.json()
        face_amount_high = res_json_high["payload"]["fnlCcPrm"]

        serializer_data = {
            "travel_request": insurance_request,
            "company": INSURANCE_COMPANY,
            "is_success": True,
            "face_amount_low": face_amount_low,
            "face_amount_mid": face_amount_mid,
            "face_amount_high": face_amount_high,
            "res_json_low": json.dumps(res_json_low),
            "res_json_mid": json.dumps(res_json_mid),
            "res_json_high": json.dumps(res_json_high),
        }

        return serializer_data
