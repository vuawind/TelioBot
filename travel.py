import os
from time import time
from datetime import datetime
from slack_bolt import App, Ack
from slack import WebClient

class travel_bot:
    TRAVEL_BLOCK={
        "title": {
            "type": "plain_text",
            "text": "Travel Request"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "callback_id": "view_travel",
        "blocks": [
            {
                "type": "actions",
                "block_id": "block_invoice",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Thêm thời gian công tác",
                            "emoji": True
                        },
                        "value": "click_me_123",
                        "action_id": "extend"
                    }
                ]
            },
            {
                "type": "input",
                "block_id": "block_user_input",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select users",
                        "emoji": True
                    },
                    "action_id": "user_select"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Approver/Người phê duyệt",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_a",
                "label": {
                    "type": "plain_text",
                    "text": "Pick a date for departure/Chọn ngày đi:"
                },
                "element": {
                    "type": "datepicker",
                    "initial_date": datetime.today().strftime('%Y-%m-%d'),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date"
                    },
                    "action_id": "departure"
                }
            },
            {
                "type": "input",
                "block_id": "block_b",
                "label": {
                    "type": "plain_text",
                    "text": "Pick a date for return/Chọn ngày về:"
                },
                "element": {
                    "type": "datepicker",
                    "initial_date": datetime.today().strftime('%Y-%m-%d'),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date"
                    },
                    "action_id": "return"
                }
            },
            {
                "type": "section",
                "block_id": "block_from",
                "text": {
                    "type": "mrkdwn",
                    "text": "*From/Từ:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hà Nội",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hồ Chí Minh",
                                "emoji": True,
                            },
                            "value": "value-2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Đà Nẵng",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hải Phòng",
                                "emoji": True,
                            },
                            "value": "value-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Cần Thơ",
                                "emoji": True,
                            },
                            "value": "value-4"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Other/Khác(include in reason/thêm địa điểm ở bảng lý do)",
                                "emoji": True,
                            },
                            "value": "value-3"
                        }
                    ],
                    "action_id": "from_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_return",
                "text": {
                    "type": "mrkdwn",
                    "text": "*To/Đến:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hà Nội",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hồ Chí Minh",
                                "emoji": True,
                            },
                            "value": "value-2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Đà Nẵng",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hải Phòng",
                                "emoji": True,
                            },
                            "value": "value-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Cần Thơ",
                                "emoji": True,
                            },
                            "value": "value-4"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Other/Khác(include in reason/thêm địa điểm ở bảng lý do)",
                                "emoji": True,
                            },
                            "value": "value-3"
                        }
                    ],
                    "action_id": "to_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_vehicle",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Vehicle/Phương tiện:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Airlane/Máy bay",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Car/Ô tô",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Bus/Xe buýt",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Train/Tàu hỏa",
                                "emoji": True,
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "vehicle_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_class",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Class/Chức vụ*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "A - Director/Giám đốc điều hành",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "B - Manager/Quản lý bộ phận",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "C - Employee/Nhân viên",
                                "emoji": True,
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "class_select"
                }
            },
            {
                "block_id": "block_id",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Your ID/ID của bạn"
                    },
                    "action_id": "input_id"
                },
                "label": {
                    "type": "plain_text",
                    "text": "ID or Passport number/CCCD hoặc hộ chiếu",
                    "emoji": True,
                }
            },
            {
                "block_id": "block_d",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Please include your preferred time of travel/Xin hãy thêm giờ đi và về"
                    },
                    "action_id": "reason_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Reason for travel/Lý do đi công tác(Thêm địa điểm nếu như chọn khác)"
                }
            },
            {
                "type": "section",
                "block_id": "block_perdiem",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Per diem/Phụ cấp*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Yes/Có",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "No/Không",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                    ],
                    "action_id": "perdiem_select"
                } 
            },
            {
                "block_id": "block_bank",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "min_length": 0,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Include bank name, location, and account number/Thêm thông tin ngân hàng(tên, chi nhánh, STK)"
                    },
                    "action_id": "bank_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Bank information/Thông tin ngân hàng"
                }
            }
        ],
    "type": "modal"
    }

    TRAVEL_BLOCK1={
        "title": {
            "type": "plain_text",
            "text": "Travel Request"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "callback_id": "view_travel",
        "blocks": [
            {
                "type": "actions",
                "block_id": "block_invoice",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Thêm thời gian công tác",
                            "emoji": True
                        },
                        "value": "click_me_123",
                        "action_id": "extend"
                    }
                ]
            },
            {
                "type": "input",
                "block_id": "block_user_input",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select users",
                        "emoji": True
                    },
                    "action_id": "user_select"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Approver/Người phê duyệt",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_a",
                "label": {
                    "type": "plain_text",
                    "text": "Pick a date for departure/Chọn ngày đi:"
                },
                "element": {
                    "type": "datepicker",
                    "initial_date": datetime.today().strftime('%Y-%m-%d'),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date"
                    },
                    "action_id": "departure"
                }
            },
            {
                "type": "input",
                "block_id": "block_b",
                "label": {
                    "type": "plain_text",
                    "text": "Pick a date for return/Chọn ngày về:"
                },
                "element": {
                    "type": "datepicker",
                    "initial_date": datetime.today().strftime('%Y-%m-%d'),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date"
                    },
                    "action_id": "return"
                }
            },
            {
                "type": "section",
                "block_id": "block_from",
                "text": {
                    "type": "mrkdwn",
                    "text": "*From/Từ:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hà Nội",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hồ Chí Minh",
                                "emoji": True,
                            },
                            "value": "value-2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Đà Nẵng",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hải Phòng",
                                "emoji": True,
                            },
                            "value": "value-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Cần Thơ",
                                "emoji": True,
                            },
                            "value": "value-4"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Other/Khác(include in reason/thêm địa điểm ở bảng lý do)",
                                "emoji": True,
                            },
                            "value": "value-3"
                        }
                    ],
                    "action_id": "from_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_return",
                "text": {
                    "type": "mrkdwn",
                    "text": "*To/Đến:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hà Nội",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hồ Chí Minh",
                                "emoji": True,
                            },
                            "value": "value-2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Đà Nẵng",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hải Phòng",
                                "emoji": True,
                            },
                            "value": "value-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Cần Thơ",
                                "emoji": True,
                            },
                            "value": "value-4"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Other/Khác(include in reason/thêm địa điểm ở bảng lý do)",
                                "emoji": True,
                            },
                            "value": "value-3"
                        }
                    ],
                    "action_id": "to_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_vehicle",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Vehicle/Phương tiện:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Airlane/Máy bay",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Car/Ô tô",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Bus/Xe buýt",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Train/Tàu hỏa",
                                "emoji": True,
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "vehicle_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_class",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Class/Chức vụ*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "A - Director/Giám đốc điều hành",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "B - Manager/Quản lý bộ phận",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "C - Employee/Nhân viên",
                                "emoji": True,
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "class_select"
                }
            },
            {
                "block_id": "block_id",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Your ID/ID của bạn"
                    },
                    "action_id": "input_id"
                },
                "label": {
                    "type": "plain_text",
                    "text": "ID or Passport number/CCCD hoặc hộ chiếu",
                    "emoji": True,
                }
            },
            {
                "block_id": "block_d",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Please include your preferred time of travel/Xin hãy thêm giờ đi và về"
                    },
                    "action_id": "reason_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Reason for travel/Lý do đi công tác(Thêm địa điểm nếu như chọn khác)"
                }
            },
            {
                "type": "section",
                "block_id": "block_perdiem",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Per diem/Phụ cấp*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Yes/Có",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "No/Không",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                    ],
                    "action_id": "perdiem_select"
                } 
            }
        ],
    "type": "modal"
    }

    TRAVEL_BLOCK_EXTEND={
        "title": {
            "type": "plain_text",
            "text": "Travel Request Extend"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "callback_id": "view_extend",
        "blocks": [
            {
                "block_id": "block_invoice",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Số ts của bạn"
                    },
                    "action_id": "input_invoice"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Điền số ts ở đây",
                    "emoji": True,
                }
            },
            {
                "type": "input",
                "block_id": "block_user_input",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select users",
                        "emoji": True
                    },
                    "action_id": "user_select"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Approver/Người phê duyệt",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_a",
                "label": {
                    "type": "plain_text",
                    "text": "Pick a date for departure/Chọn ngày đi:"
                },
                "element": {
                    "type": "datepicker",
                    "initial_date": datetime.today().strftime('%Y-%m-%d'),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date"
                    },
                    "action_id": "departure"
                }
            },
            {
                "type": "input",
                "block_id": "block_b",
                "label": {
                    "type": "plain_text",
                    "text": "Pick a date for return/Chọn ngày về:"
                },
                "element": {
                    "type": "datepicker",
                    "initial_date": datetime.today().strftime('%Y-%m-%d'),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date"
                    },
                    "action_id": "return"
                }
            },
            {
                "type": "section",
                "block_id": "block_from",
                "text": {
                    "type": "mrkdwn",
                    "text": "*From/Từ:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hà Nội",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hồ Chí Minh",
                                "emoji": True,
                            },
                            "value": "value-2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Đà Nẵng",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hải Phòng",
                                "emoji": True,
                            },
                            "value": "value-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Cần Thơ",
                                "emoji": True,
                            },
                            "value": "value-4"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Other/Khác(include in reason/thêm địa điểm ở bảng lý do)",
                                "emoji": True,
                            },
                            "value": "value-3"
                        }
                    ],
                    "action_id": "from_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_return",
                "text": {
                    "type": "mrkdwn",
                    "text": "*To/Đến:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hà Nội",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hồ Chí Minh",
                                "emoji": True,
                            },
                            "value": "value-2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Đà Nẵng",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hải Phòng",
                                "emoji": True,
                            },
                            "value": "value-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Cần Thơ",
                                "emoji": True,
                            },
                            "value": "value-4"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Other/Khác(include in reason/thêm địa điểm ở bảng lý do)",
                                "emoji": True,
                            },
                            "value": "value-3"
                        }
                    ],
                    "action_id": "to_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_vehicle",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Vehicle/Phương tiện:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Airlane/Máy bay",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Car/Ô tô",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Bus/Xe buýt",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Train/Tàu hỏa",
                                "emoji": True,
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "vehicle_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_class",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Class/Chức vụ*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "A - Director/Giám đốc điều hành",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "B - Manager/Quản lý bộ phận",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "C - Employee/Nhân viên",
                                "emoji": True,
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "class_select"
                }
            },
            {
                "block_id": "block_id",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Your ID/ID của bạn"
                    },
                    "action_id": "input_id"
                },
                "label": {
                    "type": "plain_text",
                    "text": "ID or Passport number/CCCD hoặc hộ chiếu",
                    "emoji": True,
                }
            },
            {
                "block_id": "block_d",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Please include your preferred time of travel/Xin hãy thêm giờ đi và về"
                    },
                    "action_id": "reason_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Reason for travel/Lý do đi công tác(Thêm địa điểm nếu như chọn khác)"
                }
            },
            {
                "type": "section",
                "block_id": "block_perdiem_extend",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Per diem/Phụ cấp*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Yes/Có",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "No/Không",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                    ],
                    "action_id": "extend_perdiem_select"
                } 
            },
            {
                "block_id": "block_bank",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "min_length": 0,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Include bank name, location, and account number/Thêm thông tin ngân hàng(tên, chi nhánh, STK)"
                    },
                    "action_id": "bank_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Bank information/Thông tin ngân hàng"
                }
            }
        ],
    "type": "modal"
    }

    TRAVEL_BLOCK_EXTEND1={
        "title": {
            "type": "plain_text",
            "text": "Travel Request Extend"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "callback_id": "view_extend",
        "blocks": [
            {
                "block_id": "block_invoice",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Số ts của bạn"
                    },
                    "action_id": "input_invoice"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Điền số ts ở đây",
                    "emoji": True,
                }
            },
            {
                "type": "input",
                "block_id": "block_user_input",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select users",
                        "emoji": True
                    },
                    "action_id": "user_select"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Approver/Người phê duyệt",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_a",
                "label": {
                    "type": "plain_text",
                    "text": "Pick a date for departure/Chọn ngày đi:"
                },
                "element": {
                    "type": "datepicker",
                    "initial_date": datetime.today().strftime('%Y-%m-%d'),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date"
                    },
                    "action_id": "departure"
                }
            },
            {
                "type": "input",
                "block_id": "block_b",
                "label": {
                    "type": "plain_text",
                    "text": "Pick a date for return/Chọn ngày về:"
                },
                "element": {
                    "type": "datepicker",
                    "initial_date": datetime.today().strftime('%Y-%m-%d'),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date"
                    },
                    "action_id": "return"
                }
            },
            {
                "type": "section",
                "block_id": "block_from",
                "text": {
                    "type": "mrkdwn",
                    "text": "*From/Từ:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hà Nội",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hồ Chí Minh",
                                "emoji": True,
                            },
                            "value": "value-2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Đà Nẵng",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hải Phòng",
                                "emoji": True,
                            },
                            "value": "value-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Cần Thơ",
                                "emoji": True,
                            },
                            "value": "value-4"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Other/Khác(include in reason/thêm địa điểm ở bảng lý do)",
                                "emoji": True,
                            },
                            "value": "value-3"
                        }
                    ],
                    "action_id": "from_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_return",
                "text": {
                    "type": "mrkdwn",
                    "text": "*To/Đến:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hà Nội",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hồ Chí Minh",
                                "emoji": True,
                            },
                            "value": "value-2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Đà Nẵng",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hải Phòng",
                                "emoji": True,
                            },
                            "value": "value-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Cần Thơ",
                                "emoji": True,
                            },
                            "value": "value-4"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Other/Khác(include in reason/thêm địa điểm ở bảng lý do)",
                                "emoji": True,
                            },
                            "value": "value-3"
                        }
                    ],
                    "action_id": "to_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_vehicle",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Vehicle/Phương tiện:*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Airlane/Máy bay",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Car/Ô tô",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Bus/Xe buýt",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Train/Tàu hỏa",
                                "emoji": True,
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "vehicle_select"
                }
            },
            {
                "type": "section",
                "block_id": "block_class",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Class/Chức vụ*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "A - Director/Giám đốc điều hành",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "B - Manager/Quản lý bộ phận",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "C - Employee/Nhân viên",
                                "emoji": True,
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "class_select"
                }
            },
            {
                "block_id": "block_id",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Your ID/ID của bạn"
                    },
                    "action_id": "input_id"
                },
                "label": {
                    "type": "plain_text",
                    "text": "ID or Passport number/CCCD hoặc hộ chiếu",
                    "emoji": True,
                }
            },
            {
                "block_id": "block_d",
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Please include your preferred time of travel/Xin hãy thêm giờ đi và về"
                    },
                    "action_id": "reason_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Reason for travel/Lý do đi công tác(Thêm địa điểm nếu như chọn khác)"
                }
            },
            {
                "type": "section",
                "block_id": "block_perdiem_extend",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Per diem/Phụ cấp*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Yes/Có",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "No/Không",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                    ],
                    "action_id": "extend_perdiem_select"
                } 
            }
        ],
    "type": "modal"
    }

    SEND_INFO = {
        "title": {
            "type": "plain_text",
            "text": "Travel Information"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "callback_id": "view_info",
        "blocks": [
            {
                "type": "input",
                "block_id": "block_a_input",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select users",
                        "emoji": True
                    },
                    "action_id": "user_select"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Requester/Người yêu cầu công tác",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "block_id": "block_b_input",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Vehicle/Phương tiện*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Car/Ô tô",
                                "emoji": True
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Bus/Xe buýt",
                                "emoji": True
                            },
                            "value": "value-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Train/Tàu hỏa",
                                "emoji": True
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Airplane/Máy bay",
                                "emoji": True
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "vehicle_select"
                }
            },
            {
                "type": "input",
                "block_id": "block_c_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "vehicle_num"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Vehicle's number or License plate/Số xe hoặc biển xe",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_d_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "driver_name"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Driver's name/Tên người lái",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_e_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "driver_num"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Driver's number/Số điện thoại người lái",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_f_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "hotel_name"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Hotel's name/Tên khách sạn",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_g_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "hotel_location"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Hotel's location/Địa chỉ khách sạn",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_h_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "hotel_num"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Hotel's booking number/Số booking khách sạn",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_l_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "flight_ticket"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Flight ticket/Vé máy bay",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_j_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "boarding_pass"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Boarding pass/Thẻ máy bay",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_k_input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "note_id"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Note/Ghi chú",
                    "emoji": True
                }
            }
        ],
        "type": "modal"
    }
