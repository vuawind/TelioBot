import os
from time import time
from datetime import datetime
from slack_bolt import App, Ack
from slack import WebClient

class welcome:
    WELCOME_MODAL={
        "title": {
        "type": "plain_text",
        "text": "Sophie Bot"
        },
        "callback_id": "view_travel",
        "blocks": [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Đưa tôi đến Sophie",
                            "emoji": True
                        },
                        "value": "sophie",
                        "url": "https://teliovn.slack.com/archives/D024MFB2B1D",
                        "action_id": "sophie"
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "*Hoặc check tin nhắn từ TelioBot*"
                    }
                ]
            },
            {
                "type": "image",
                "image_url": "https://i1.wp.com/thetempest.co/wp-content/uploads/2017/08/The-wise-words-of-Michael-Scott-Imgur-2.jpg?w=1024&ssl=1",
                "alt_text": "inspiration"
            }
        ],
        "type": "modal"
    }
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
                            "text": "IV. Bảo hiểm",
                            "emoji": True
                        },
                        "value": "click4",
                        "action_id": "insurance_id"
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
                            "text": "V. Thuế",
                            "emoji": True
                        },
                        "value": "click5",
                        "action_id": "tax_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "VI. Chấm công - Tính lương",
                            "emoji": True
                        },
                        "value": "click6",
                        "action_id": "salary_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "VII. Kỷ luật lao động",
                            "emoji": True
                        },
                        "value": "click7",
                        "action_id": "work_id"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "VIII. Câu hỏi khác",
                            "emoji": True
                        },
                        "value": "click8",
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
								"text": "1.Thủ tục onboard/tiếp nhận nhân viên mới như thế nào?",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2.Nhân viên Telio mới cần làm những thủ tục gì?",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3.Thông tin về email và tài khoản 1 office?",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4.Nếu có thắc mắc về chế độ chính sách thì liên hệ ai?",
								"emoji": True
							},
							"value": "value-3"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5.Bộ hồ sơ nhân sự bao gồm những gì?",
								"emoji": True
							},
							"value": "value-4"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6.Công ty thanh toán lương như thế nào?",
								"emoji": True
							},
							"value": "value-5"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7.Làm thế nào để tìm Số điện thoại và Email của đồng nghiệp?",
								"emoji": True
							},
							"value": "value-6"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "8.Cách sử dụng slack như thế nào?",
								"emoji": True
							},
							"value": "value-7"
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
								"text": "2. Nếu nghỉ việc thì thời gian nhận khoản lương còn lại là khi nào?",
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
								"text": "4. Nghỉ việc có được thanh toán phép tồn khi nghỉ việc không?",
								"emoji": True
							},
							"value": "value-3"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5. Bao giờ được trả sổ BHXH đã chốt khi nghỉ việc?",
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
				"text": "IV. Bảo hiểm"
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
								"text": "1. Danh mục các bệnh viện được đăng ký khám chữa bệnh?",
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
								"text": "3. Thủ tục và quyền lợi chế độ thai sản?",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4. Thủ tục và quyền lợi chế độ dưỡng sức?",
								"emoji": True
							},
							"value": "value-3"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5. Đã có thẻ BH tự nguyện hoặc thẻ BH theo hộ gia đình?",
								"emoji": True
							},
							"value": "value-4"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6. Tôi đã mua Bảo hiểm nhân thọ/ Bảo hiểm sức khỏe?",
								"emoji": True
							},
							"value": "value-5"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7. Đang ký HĐLĐ và tham gia Bảo hiểm xã hội tại công ty khác?",
								"emoji": True
							},
							"value": "value-6"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "8. Sai thông tin cá nhân trên sổ BHXH, thẻ BHYT thì có cần làm thủ tục?",
								"emoji": True
							},
							"value": "value-7"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9. Thay đổi số CMTND hoặc căn cước công dân?",
								"emoji": True
							},
							"value": "value-8"
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

    BLOCK_TAX = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "V. Thuế"
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
				"text": "VI. Chấm công - Tính lương"
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
								"text": "2. Các đối tượng được tự động/miễn chấm công",
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
								"text": "4. Trường hợp nghỉ việc để chăm con ốm thông thường",
								"emoji": True
							},
							"value": "value-3"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5. Trường hợp nghỉ ốm thông thường",
								"emoji": True
							},
							"value": "value-4"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6. Trường hợp quá hạn 5 ngày không tạo đơn được",
								"emoji": True
							},
							"value": "value-5"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "7. Nếu muốn xem số ngày phép tồn đến thời điểm hiện tại?",
								"emoji": True
							},
							"value": "value-6"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "8. Bản thân kết hôn thì được hưởng những quyền lợi gì?",
								"emoji": True
							},
							"value": "value-7"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "9. Quyền lợi khi sinh con hoặc vợ sinh con?",
								"emoji": True
							},
							"value": "value-8"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "10. Công ty có chế độ gì cho ngày sinh nhật không?",
								"emoji": True
							},
							"value": "value-9"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "11. Nếu gia đình có người mất, công ty có phúc lợi gì không?",
								"emoji": True
							},
							"value": "value-10"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "12. Trường hợp nhân viên bị ốm đau, tai nạn?",
								"emoji": True
							},
							"value": "value-11"
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
								"text": "3. Muốn xem Nội quy lao động thì cần xem ở đâu?",
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
