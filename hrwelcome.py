import os
from time import time
from datetime import datetime
from slack_bolt import App, Ack
from slack import WebClient

class welcome:
    WELCOME_BLOCK = [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "I. Onboard",
                            "emoji": True
                        },
                        "value": "click1",
                        "action_id": "onboard_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "II. Nghỉ việc",
                            "emoji": True
                        },
                        "value": "click2",
                        "action_id": "quitjob_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "III. Điều chuyển, thăng chức",
                            "emoji": True
                        },
                        "value": "click3",
                        "action_id": "move_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "IV. Bảo hiểm/Khám chữa bệnh",
                            "emoji": True
                        },
                        "value": "click4",
                        "action_id": "insurance_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "V. Thai sản",
                            "emoji": True
                        },
                        "value": "click5",
                        "action_id": "pregnant_id"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "VI. Thuế",
                            "emoji": True
                        },
                        "value": "click6",
                        "action_id": "tax_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "VII. Chấm công - Tính lương",
                            "emoji": True
                        },
                        "value": "click7",
                        "action_id": "salary_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "VIII. Ngày nghỉ",
                            "emoji": True
                        },
                        "value": "click8",
                        "action_id": "off_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "IX. Kỷ luật lao động",
                            "emoji": True
                        },
                        "value": "click9",
                        "action_id": "work_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "X. Câu hỏi khác",
                            "emoji": True
                        },
                        "value": "click10",
                        "action_id": "other_id"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]

    BLOCK_ONBOARD = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "I. Onboarding"
			}
		},
		{
			"type": "actions",
            "block_id": "block_a",
			"elements":[
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Tìm câu hỏi tại đây",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "1. Nhân viên mới cần làm những gì?",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2. Email Telio và tài khoản 1office của tôi?",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3. Tôi cần hỗ trợ về khóa học E-Learn Đào tạo hội nhập",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4. Về thủ tục onboard nhân viên mới?",
								"emoji": True
							},
							"value": "value-3"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5. Bộ hồ sơ nhân sự gồm những gì?",
								"emoji": True
							},
							"value": "value-4"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6. Công ty thanh toán lương như thế nào?",
								"emoji": True
							},
							"value": "value-5"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7. Tôi phải thông báo STK Ngân hàng cho ai?",
								"emoji": True
							},
							"value": "value-6"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "8. Tôi muốn tìm SĐT & Email của đồng nghiệp?",
								"emoji": True
							},
							"value": "value-7"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9. Cách sử dụng slack?",
								"emoji": True
							},
							"value": "value-8"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "10. Khi nào tôi sẽ nhận được lương?",
								"emoji": True
							},
							"value": "value-9"
						}
					],
					"action_id": "onboard_select"
				}
            ]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				}
			]
		},
		{
			"type": "divider"
		}
    ]
    
    BLOCK_QUIT = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "II. Nghỉ việc"
			}
		},
		{
			"type": "actions",
            "block_id": "block_b",
			"elements":[
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Tìm câu hỏi tại đây",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "1. Thủ tục nghỉ việc như thế nào?",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2. Khi nào tôi nhận được tháng lương cuối cùng?",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3. Thủ tục hưởng Bảo hiểm thất nghiệp?",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4. Tôi có được thanh toán tiền cho ngày phép còn lại?",
								"emoji": True
							},
							"value": "value-3"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5. Tôi sẽ nhận được sổ BHXH đã chốt khi nào?",
								"emoji": True
							},
							"value": "value-4"
						}
					],
					"action_id": "quit_select"
				}
            ]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				}
			]
		},
		{
			"type": "divider"
		}
    ]

    BLOCK_MOVE = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "III. Điều chuyển, thăng chức"
			}
		},
		{
			"type": "actions",
            "block_id": "block_c",
			"elements":[
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Tìm câu hỏi tại đây",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "1. Thủ tục điều chuyển nhân sự như thế nào?",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2. Thủ tục thăng chức nhân sự như thế nào?",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3. Thông tin đề xuất thăng chức, điều chuyển thông tin cho ai?",
								"emoji": True
							},
							"value": "value-2"
						}
					],
					"action_id": "move_select"
				}
            ]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				}
			]
		},
		{
			"type": "divider"
		}
    ]

    BLOCK_INSURANCE = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "IV. Bảo hiểm/Khám chữa bệnh"
			}
		},
		{
			"type": "actions",
            "block_id": "block_d",
			"elements":[
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Tìm câu hỏi tại đây",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "1. Danh sách bệnh viện đăng ký khám chữa bệnh?",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2. Khám bệnh thì được hưởng BHYT như thế nào?",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3. Tôi đã có thẻ BH tự nguyện/theo hộ gia đình",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4. Tôi đã mua Bảo hiểm nhân thọ/ Bảo hiểm sức khỏe?",
								"emoji": True
							},
							"value": "value-3"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5. Đang ký HĐLĐ và tham gia BHXH tại công ty khác?",
								"emoji": True
							},
							"value": "value-4"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6. Sai thông tin trên sổ BHXH, thẻ BHYT thì làm như thế nào?",
								"emoji": True
							},
							"value": "value-5"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7. Thay đổi số CMTND hoặc căn cước công dân?",
								"emoji": True
							},
							"value": "value-6"
						}
					],
					"action_id": "insurance_select"
				}
            ]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				}
			]
		},
		{
			"type": "divider"
		}
    ]

    BLOCK_PREGNANT = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "V. Thai sản"
			}
		},
		{
			"type": "actions",
            "block_id": "block_preg",
			"elements":[
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Tìm câu hỏi tại đây",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "1. Về chế độ thai sản?",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2. Về chế độ dưỡng sức sau thai sản?",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3. Tôi sinh con hoặc Vợ sinh con thì được hưởng quyền lợi gì?",
								"emoji": True
							},
							"value": "value-2"
						}
					],
					"action_id": "pregnant_select"
				}
            ]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				}
			]
		},
		{
			"type": "divider"
		}
    ]

    BLOCK_TAX = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "VI. Thuế"
			}
		},
		{
			"type": "actions",
            "block_id": "block_e",
			"elements":[
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Tìm câu hỏi tại đây",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "1. Thủ tục đăng ký Người phụ thuộc?",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2. Tại sao phải trích thuế TNCN 10% khi ký hợp đồng",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3. Có từ 2 mã số thuế trở lên, cần làm thủ tục gì để gộp MST?",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4. Thay đổi số CMTND có cần thay đổi thông tin trên MST hay không?",
								"emoji": True
							},
							"value": "value-3"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5. Thủ tục tự Quyết toán thuế tại cơ quan thuế như thế nào?",
								"emoji": True
							},
							"value": "value-4"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6. Làm thế nào để tra cứu số thuế?",
								"emoji": True
							},
							"value": "value-5"
						}
					],
					"action_id": "tax_select"
				}
            ]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				}
			]
		},
		{
			"type": "divider"
		}
    ]

    BLOCK_SALARY = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "VII. Chấm công - Tính lương"
			}
		},
		{
			"type": "actions",
            "block_id": "block_f",
			"elements":[
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Tìm câu hỏi tại đây",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "1. Quy định hiện tại về chấm công?",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2. Ai sẽ được miễn chấm công?",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3. Hướng dẫn tạo các loại đơn trên 1 Office",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4. Hướng dẫn cách duyệt đơn trên 1 Office",
								"emoji": True
							},
							"value": "value-3"
						}
					],
					"action_id": "salary_select"
				}
            ]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				}
			]
		},
		{
			"type": "divider"
		}
    ]

    BLOCK_OFF = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "VIII. Ngày nghỉ"
			}
		},
		{
			"type": "actions",
            "block_id": "block_off",
			"elements":[
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Tìm câu hỏi tại đây",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "1. Tôi nghỉ việc để chăm con ốm thì tạo đơn nghỉ gì?",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2. Tôi nghỉ ốm thì tạo đơn gì?",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3. Tôi làm gì khi không tạo được đơn do quá hạn 5 ngày?",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4. Tôi muốn xem số ngày phép tồn đến thời điểm hiện tại?",
								"emoji": True
							},
							"value": "value-3"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5. Tôi kết hôn thì được hưởng những quyền lợi gì?",
								"emoji": True
							},
							"value": "value-4"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6. Quyền lợi khi sinh con hoặc Vợ sinh con?",
								"emoji": True
							},
							"value": "value-5"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7. Công ty có chế độ gì cho ngày sinh nhật không?",
								"emoji": True
							},
							"value": "value-6"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "8. Gia đình tôi có người mất, công ty có phúc lợi gì không?",
								"emoji": True
							},
							"value": "value-7"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9. Tôi bị ốm đau, tai nạn, công ty có chế độ thăm hỏi gì không?",
								"emoji": True
							},
							"value": "value-8"
						}
					],
					"action_id": "off_select"
				}
            ]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				}
			]
		},
		{
			"type": "divider"
		}
    ]

    BLOCK_WORK = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "VII. Kỷ luật lao động"
			}
		},
		{
			"type": "actions",
            "block_id": "block_g",
			"elements":[
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Tìm câu hỏi tại đây",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "1. Khi có phát sinh về kỷ luật lao động cần liên hệ ai?",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2. Quy trình xử lý kỷ luật như thế nào?",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3. Tôi muốn xem Nội quy lao động?",
								"emoji": True
							},
							"value": "value-2"
						}
					],
					"action_id": "work_select"
				}
            ]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				}
			]
		},
		{
			"type": "divider"
		}
    ]

    BLOCK_OTHER = [
		{
			"type": "input",
            "label": {
                "type": "plain_text",
                "text": "VIII. Câu hỏi khác",
                "emoji": True
            },
            "block_id": "block_h",
			"element": {
                "type": "plain_text_input",
                "multiline": True,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Câu hỏi này sẽ được gửi đến HR",
                    "emoji": True
                },
                "action_id": "other_input"
            }
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back/Quay lại",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Submit/Nộp",
						"emoji": True
					},
					"value": "click_submit",
					"action_id": "submit"
				}
			]
		},
		{
			"type": "divider"
		}
    ]
