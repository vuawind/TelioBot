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
                    "text": "User",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "block_a",
                "label": {
                    "type": "plain_text",
                    "text": "Pick a date for departure:"
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
                    "text": "Pick a date for return:"
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
                    "text": "*From:*"
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
                                "text": "Other (Please state your destination in the reason for travel box)",
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
                    "text": "*To:*"
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
                                "text": "Other (Please state your destination in the reason for travel box)",
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
                    "text": "*Vehicle:*"
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
                                "text": "Plane",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Car",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Train",
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
                    "text": "*Class*"
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
                                "text": "A - Director",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "B - Manager",
                                "emoji": True,
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "C - Employee",
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
                        "text": "Your ID"
                    },
                    "action_id": "input_id"
                },
                "label": {
                    "type": "plain_text",
                    "text": "ID or Passport number",
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
                        "text": "Please include your preferred time of travel"
                    },
                    "action_id": "reason_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Reason for travel"
                }
            },
            {
                "type": "section",
                "block_id": "block_perdiem",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Per diem*"
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
                                "text": "Yes",
                                "emoji": True,
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "No",
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
                        "text": "Input bank information including name, bank location, and account number"
                    },
                    "action_id": "bank_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Bank information"
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
                    "text": "User",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "block_id": "block_b_input",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Vehicle*"
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
                                "text": "Car",
                                "emoji": True
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Train",
                                "emoji": True
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Airplane",
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
                    "text": "Vehicle's number or License plate",
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
                    "text": "Driver's name",
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
                    "text": "Driver's number",
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
                    "text": "Hotel's name",
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
                    "text": "Hotel's location",
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
                    "text": "Hotel's booking number",
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
                    "text": "Boarding pass",
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
                    "text": "Note",
                    "emoji": True
                }
            }
        ],
        "type": "modal"
    }