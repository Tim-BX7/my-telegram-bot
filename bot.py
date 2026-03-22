import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# جلب التوكن من إعدادات البيئة في Railway
# تأكد من إضافة متغير باسم TOKEN في لوحة تحكم Railway
TOKEN = os.getenv("TOKEN")

user_path = {}
DATA = {
"🎓 السنة الثالثة":{
"📖 الفصل الثاني":{
"💻 هندسة البرمجيات":{

"📄 النظري":{

"📚 كميت":[
("هندسة 1","BQACAgIAAxkBAAIBv2m8QerIa6Rl9ONwAZn2b_0OPEVKAAJIpQACTejhSexyIatCBct4OgQ"),
("هندسة 2","BQACAgIAAxkBAAIBwGm8QepaThoaIg8neyQjKnZlZHHuAAJJpQACTejhSQsSUf3wWnmKOgQ"),
("هندسة 3","BQACAgIAAxkBAAIBwWm8QepclJJ449tn6QABQK2qlJMrpwACS6UAAk3o4UmeVRBMzzs6XzoE"),
("هندسة 4","BQACAgIAAxkBAAIBwmm8QerW30-7Xjlf3NizHS2LI8Z2AAJNpQACTejhSdfPLEVmdFlxOgQ"),
("هندسة 5","BQACAgIAAxkBAAIBw2m8QerQn4zgXOtsCXxwRaLbEJnqAAJRpQACTejhScuGrbeK68AeOgQ"),
("هندسة 6","BQACAgIAAxkBAAIBxGm8Qeoj2XV1KlSi6mw1S3w9AqIPAAJXpQACTejhSano2eOiS0l7OgQ"),
("هندسة 7","BQACAgIAAxkBAAIBxWm8Qeq1BqQfHBhN31RTLCZ5643AAJdpQACTejhSdguUkHhbIYOOgQ"),
("هندسة 8","BQACAgIAAxkBAAIBxmm8Qeq0FZpPRa6lI5tGXSbEEzHTAAJfpQACTejhST9TtJ6ZvcGWOgQ"),
("هندسة 9","BQACAgIAAxkBAAIBvmm8QeomzHbpqOq9w_z5-VUfjJqkAAJHpQACTejhSTkprNGcsN0eOgQ"),
],

"📚 غيت":[
("هندسة 1","BQACAgIAAxkBAAIBv2m8QerIa6Rl9ONwAZn2b_0OPEVKAAJIpQACTejhSexyIatCBct4OgQ"),
("هندسة 2","BQACAgIAAxkBAAIBwGm8QepaThoaIg8neyQjKnZlZHHuAAJJpQACTejhSQsSUf3wWnmKOgQ"),
("هندسة 3","BQACAgIAAxkBAAIBwWm8QepclJJ449tn6QABQK2qlJMrpwACS6UAAk3o4UmeVRBMzzs6XzoE"),
("هندسة 4","BQACAgIAAxkBAAIBwmm8QerW30-7Xjlf3NizHS2LI8Z2AAJNpQACTejhSdfPLEVmdFlxOgQ"),
("هندسة 5","BQACAgIAAxkBAAIBw2m8QerQn4zgXOtsCXxwRaLbEJnqAAJRpQACTejhScuGrbeK68AeOgQ"),
("هندسة 6","BQACAgIAAxkBAAIBxGm8Qeoj2XV1KlSi6mw1S3w9AqIPAAJXpQACTejhSano2eOiS0l7OgQ"),
("هندسة 7","BQACAgIAAxkBAAIBxWm8Qeq1BqQfHBhN31RTLCZ5643AAJdpQACTejhSdguUkHhbIYOOgQ"),
("هندسة 8","BQACAgIAAxkBAAIBxmm8Qeq0FZpPRa6lI5tGXSbEEzHTAAJfpQACTejhST9TtJ6ZvcGWOgQ"),
]
},

"🧪 العملي":{

"📚 غيت":[
("نوطة","BQACAgIAAxkBAAIBrGm8P5lyTyZMBY1zxUihtiS7UxHwAAI2pQACTejhSWPTkJKB9XcyOgQ"),
("جلسة 1","BQACAgIAAxkBAAIBrWm8P5kQCvJW1ixp0ZvbKolVUQE3AAI3pQACTejhSRT2xulNXgABXzoE"),
("جلسة 2","BQACAgIAAxkBAAIBrmm8P5k0F_CWnFp71zqJbe1TSGz_AAI5pQACTejhSb2npave4nGDOgQ"),
("جلسة 3","BQACAgIAAxkBAAIBr2m8P5kbsgg0TqhMLfYZtrUCW1wfAAI7pQACTejhSZBtDQmSHKUHOgQ"),
("جلسة 4","BQACAgIAAxkBAAIBsGm8P5l60H-wO5CwFN7u1b95IiFNAAI8pQACTejhScmtfPYTc8PmOgQ"),
("جلسة 5","BQACAgIAAxkBAAIBsWm8P5kJ9AVG9336qFGfSAQlC-JVAAI-pQACTejhST8L_M62VqriOgQ"),
("جلسة 6","BQACAgIAAxkBAAIBsmm8P5lV53Kluuw6ngzK8ZghZW5xAAI_pQACTejhSQIkNsusm75WOgQ"),
("جلسة 7","BQACAgIAAxkBAAIBs2m8P5nhFZZ1lb0nv8ITRrs-hECaAAJFpQACTejhSQIGQmTIdQ_YOgQ"),
],

"📚 كميت":[
("جلسة 1","BQACAgIAAxkBAAIBo2m8PXWz5S4uYC8l-EN30OUN5EIuAAIipQACTejhSUOHkWE6BPqzOgQ"),
("جلسة 2","BQACAgIAAxkBAAIBpGm8PXVbl9BbCJIagXF7wpyaPCUiAAIlpQACTejhSYCFtMKiygilOgQ"),
("جلسة 3","BQACAgIAAxkBAAIBpWm8PXXYBt7uaUHEjvwIA3nMjV89AAIupQACTejhSQRh3bI2b3VoOgQ"),
("جلسة 4","BQACAgIAAxkBAAIBomm8PXVN6B7Hg8Shq0Mil4GzAAGsJgACIKUAAk3o4UmAM0E_e5PcSjoE"),
]

}

},
"🧬 نظرية المعلومات":{

"📄 النظري":{

"📚 غيت":[
("معلومات 1","BQACAgIAAxkBAAIBf2m8OrP14CZrsyWDH126OYlMwo_JAAL9pAACTejhSSmbpqtgxc20OgQ"),
("معلومات 2","BQACAgIAAxkBAAIBgGm8OrP_hW3z3YvoSCK8ycNsZuP8AAIBpQACTejhSd_TSbEcDThmOgQ"),
("معلومات 3","BQACAgIAAxkBAAIBgWm8OrN_srIkZNV-lzf9X6_CcnEiAAICpQACTejhSbekaapXqUitOgQ"),
("معلومات 4","BQACAgIAAxkBAAIBgmm8OrPzD09kTgHhesfpfuS8Dr3tAAIEpQACTejhSaDWNCrWeJoDOgQ"),
("معلومات 5","BQACAgIAAxkBAAIBfmm8OrNQOoDYEATNqjohAT3O54-JAAL8pAACTejhSf5HI39K2tSHOgQ"),
],

"📚 كميت":[
("معلومات 1","BQACAgIAAxkBAAIBiWm8OzSbzt0RJDcnKSwr37JECdfFAAIJpQACTejhSWkfuR9q36tZOgQ"),
("معلومات 2","BQACAgIAAxkBAAIBimm8OzQAAZr1waPBdtkvK5nwCzKQbAACCqUAAk3o4Ul_wjpNV3mv_DoE"),
("معلومات 3","BQACAgIAAxkBAAIBi2m8OzQVEw5N_0g14o1KBYddqsOMAAILpQACTejhSY4DHiiMrsnrOgQ"),
("معلومات 5","BQACAgIAAxkBAAIBiGm8OzScknOOEDsKeajy8ekG6_47AAIIpQACTejhSbFAbiFyIDqVOgQ"),
]

},

"🧪 العملي":{

"📚 غيت":[
("دورات","BQACAgIAAxkBAAIBkGm8O2vaJGC7UHAebkulWFLoUqXAAAIMpQACTejhSbOAOmTU4huqOgQ"),
("جلسة 1+2","BQACAgIAAxkBAAIBkWm8O2sJ0-HBnSltGuer95iqQ2FEAAIOpQACTejhSSwr77sotWwCOgQ"),
("جلسة 3+4+5","BQACAgIAAxkBAAIBkmm8O2sy7dEwVL7-dSIlSntLeT-HAAIPpQACTejhSZP2l8ijqf97OgQ"),
],

"📚 كميت":[
("جلسة 1","BQACAgIAAxkBAAIBl2m8O9sWQvCI3mvi2VQ8qYP2-tt0AAIRpQACTejhSVzXcOOjPEmxOgQ"),
("جلسة 2","BQACAgIAAxkBAAIBmGm8O9vFni_7mEK4qYJOSS6RNrgwAAITpQACTejhSWNCDQpFmxxuOgQ"),
("جلسة 3","BQACAgIAAxkBAAIBmWm8O9s8Sob1mZFrGZlL71mQuPI8AAIXpQACTejhSVPJYDZDhKUaOgQ"),
("جلسة 4","BQACAgIAAxkBAAIBmmm8O9v_yJHI1oE-aJAvQDgUX0Q1AAIYpQACTejhSfCpGmzCe6qrOgQ"),
("جلسة 5","BQACAgIAAxkBAAIBlmm8O9vv7BKR5GuaKJS6OrCvAAEtigACEKUAAk3o4Unj9zhUzk5ZkjoE"),
]

}

},
"🧠 نظرية التعقيد":{

"📄 النظري":{

"📚 غيت":[
("تمارين إضافية","BQACAgIAAxkBAAIBZGm8OZ2L0Le6pgAB7c9WR7icvMCqygAC2KQAAk3o4UkAAUbxEUUHNaY6BA"),
("مكثفة امتحانية","BQACAgIAAxkBAAIBZWm8OZ2zuEGgJvMdrQpMLIVyw0inAALjpAACTejhSXx3buWPyspnOgQ"),
("تعقيد 1","BQACAgIAAxkBAAIBZmm8OZ2w7DbUnZdPlLV08XDy99lnAALopAACTejhSSGSbvyP1wQ3OgQ"),
("تعقيد 2","BQACAgIAAxkBAAIBZ2m8OZ17koBwMYrrF5H2ZoHFjxq9AALqpAACTejhSTCTN32Canb5OgQ"),
("تعقيد 3","BQACAgIAAxkBAAIBaGm8OZ09Mcmktv3shWVHJRIF6-rzAALspAACTejhSfJtEpMT2m4lOgQ"),
("تعقيد 4","BQACAgIAAxkBAAIBaWm8OZ2q3LBWqFJYLO_fczfAu3TgAALupAACTejhSfkJ-Or3K_gOOgQ"),
("تعقيد 5","BQACAgIAAxkBAAIBamm8OZ2V3XSraA2FI6GlI4gzBFH5AALvpAACTejhScOleQfnndxfOgQ"),
("تعقيد 6","BQACAgIAAxkBAAIBa2m8OZ1LBypIlXxddMTVbLvMxhgSAALxpAACTejhSb2l5pfpD-w2OgQ"),
("تعقيد 7","BQACAgIAAxkBAAIBbGm8OZ1bbybltq2pKiE8z3HNC0cxAALypAACTejhSesKyY2--WC4OgQ"),
("تعقيد 8","BQACAgIAAxkBAAIBbWm8OZ31E8fkAQ0SVK0XYSPPNQIGAALzpAACTejhSXbmmAGU5KU-OgQ"),
("تعقيد 9","BQACAgIAAxkBAAIBeGm8OjsuOiht8o1yEUiydGAsT8J2AAL1pAACTejhSdzTIiLeHhjuOgQ"),
("تعقيد 10","BQACAgIAAxkBAAIBeWm8Ojt6vpUQe6sBgHGqEgPX6kPWAAL4pAACTejhSZcvXmvL-choOgQ"),
("تعقيد 11","BQACAgIAAxkBAAIBemm8OjvjxDnASxnHAZ12W2QdfrkYAAL7pAACTejhSXibJA2FDUgXOgQ"),
],

"📚 كميت":[
("محاضرة 1","BQACAgIAAxkBAAIBVGm8N-c-E_OHzyDjxeIe3NocqeliAALEpAACTejhSf1dS2P0JHj5OgQ"),
("محاضرة 2","BQACAgIAAxkBAAIBVWm8N-c3jmee1qDWiQUylgYbgU03AALGpAACTejhSSWmcOd34fg8OgQ"),
("محاضرة 3","BQACAgIAAxkBAAIBVmm8N-eLBOuKxqqcTQXfkhyfvQiuAALIpAACTejhSVD8xx-YplpgOgQ"),
("محاضرة 4","BQACAgIAAxkBAAIBV2m8N-eXfBrx4Kk6X4nGxl57TUHtAALLpAACTejhSaXdDwTGWtCyOgQ"),
("محاضرة 5","BQACAgIAAxkBAAIBWGm8N-ePdmrZaI9vyJy4jkrlZwZDAALOpAACTejhSTpTHgcKE3uROgQ"),
("محاضرة 6","BQACAgIAAxkBAAIBWWm8N-d1MDtfNnFYVH0D-md7_tL6AALRpAACTejhSX94Wh-1wQECOgQ"),
("محاضرة 7","BQACAgIAAxkBAAIBWmm8N-dXfDlNo-tprEXxaQTjLg_iAALTpAACTejhSdL62M8VaqqfOgQ"),
("محاضرة 8","BQACAgIAAxkBAAIBW2m8N-fGB_1EGy2VYlS3hNQ7hn6FAALWpAACTejhSdE7BKitvGnbOgQ"),
]

}

},
"🌐 شبكات":{

"📄 النظري":{
"📚 غيت":[
("شبكات 1","BQACAgIAAxkBAAIBHmm8NLWNLUWzU1GbZJ_skoJW91nJAAKBpAACTejhSQhOwaYsaMVbOgQ"),
("شبكات 2","BQACAgIAAxkBAAIBH2m8NLVgkrKT4MGmNzwcGYkpyhLvAAKEpAACTejhST0k93BNsFbYOgQ"),
("شبكات 3","BQACAgIAAxkBAAIBIGm8NLW1g-nqbrXaxvQptQSv2xRRAAKIpAACTejhSd1K3zungDKtOgQ"),
("شبكات 4","BQACAgIAAxkBAAIBIWm8NLXR_dkzFg15SR0DqZQPWROoAAKKpAACTejhSYf0W2KLn9ZPOgQ"),
("شبكات 5","BQACAgIAAxkBAAIBImm8NLU3MQ7qLTip-AIRv-BJatmWAAKNpAACTejhSfmkVLY1Gt3TOgQ"),
("شبكات 6","BQACAgIAAxkBAAIBI2m8NLUjszN8RZjnGMj3InIwQf0QAAKPpAACTejhSVaCCNVzgjvsOgQ"),
("شبكات 7","BQACAgIAAxkBAAIBJGm8NLU0p_qCOXwMorIpz1C8atW7AAKRpAACTejhSVCQwQZigLCcOgQ"),
("شبكات 8","BQACAgIAAxkBAAIBJWm8NLVzJTOtLpZThF_Z3Yt0WmVDAAKapAACTejhSTj2ZTf179ebOgQ"),
("شبكات 9","BQACAgIAAxkBAAIBJmm8NLW96YB0UdfVb-me9rq_YQPdAAKepAACTejhSb91L5Cr1zxROgQ"),
],

"📚 كميت":[
("شبكات 1","BQACAgIAAxkBAAIBMGm8NWg1pmd9tVAUCmGLJ22s0qSRAAKhpAACTejhSR6mL32vPm8QOgQ"),
("شبكات 2","BQACAgIAAxkBAAIBMWm8NWhANCT5jQ1y86TPXrftRCK9AAKipAACTejhSXi7AW5qpOI2OgQ"),
("شبكات 3","BQACAgIAAxkBAAIBMmm8NWgVhdKEQ6jYfjSRHXS2IG1QAAKkpAACTejhSbPwBrGKZt73OgQ"),
("شبكات 4","BQACAgIAAxkBAAIBM2m8NWi-xVVJEn1GY1qR87SFVLp7AAKmpAACTejhSSd9Em0DEs4yOgQ"),
]
},

"🧪 العملي":{
"📚 غيت":[
("عملي 1","BQACAgIAAxkBAAIBOGm8Ne9DWX1Uwbnf8KqVxLR_j0BZAAKopAACTejhSf2kUFsWAdu8OgQ"),
("عملي 2","BQACAgIAAxkBAAIBOWm8Ne_7_o5sloy3SPCNXDjnnrsMAAKqpAACTejhSVrd7FQ-OcEYOgQ"),
("عملي 3","BQACAgIAAxkBAAIBOmm8Ne9WUug11_0UK5MmnR9yd8DyAAKrpAACTejhSSf_HYDhLl_BOgQ"),
("عملي 4","BQACAgIAAxkBAAIBO2m8Ne9PFDKlNBdJU6jJ3JtNA7XPAAKspAACTejhSc7xLDMSqKopOgQ"),
("عملي 5","BQACAgIAAxkBAAIBPGm8Ne8nBie0l--YNS8Y5IrCU7y2AAKtpAACTejhSSWMpj_FoQLoOgQ"),
("عملي 6","BQACAgIAAxkBAAIBPWm8Ne9kP4eshb0uQV4Hs2uBYwWBAAKupAACTejhST1MJtfd25_qOgQ"),
("عملي 7","BQACAgIAAxkBAAIBPmm8Ne-O9HqOYMpRs8I1Mb7C2I3kAAKvpAACTejhSa0h3xW0hoqJOgQ"),
("وايرشارك","BQACAgIAAxkBAAIBRmm8Nl2cScK5QL_mcbS1g1LJWGORAAKwpAACTejhSRpu3ghWwS1hOgQ"),
],

"📚 كميت":[
("عملي 1","BQACAgIAAxkBAAIBR2m8Nl0jzR99XuIU0zINkHm3c2BuAAKxpAACTejhSW3cATsgnQ6zOgQ"),
("عملي 2","BQACAgIAAxkBAAIBSGm8Nl1z60kKT807OIQ_Z7qPkgkTAAKypAACTejhSRIc-9mBOnSKOgQ"),
("عملي 3","BQACAgIAAxkBAAIBSWm8Nl0q8hF0RJlp8c4ZvKTxfabbAAK0pAACTejhScY3lcXdK9Z3OgQ"),
("عملي 4","BQACAgIAAxkBAAIBSmm8Nl1ykhUdmv7tMkzYJqOvTSEyAAK2pAACTejhSa2KVQoxW2wLOgQ"),
("عملي 5","BQACAgIAAxkBAAIBS2m8Nl1lSrgNtMxFYe4VMq-ZZ6VcAAK4pAACTejhSXdE6DoH-YRIOgQ"),
("عملي 6","BQACAgIAAxkBAAIBTGm8Nl2Rc26dxT1fViPS7tGef4YuAAK7pAACTejhSQ6BnbC1RQ7oOgQ"),
]
}

},
"🤖 ذكاء اصطناعي":{

"📄 النظري":{
"📚 غيت":[
("نظري 1","BQACAgIAAxkBAAIBBmm8M0HgUT64VI5Wz0WHn3Ua8GrLAAJlpAACTejhSeR5NovD1E-GOgQ"),
("نظري 2","BQACAgIAAxkBAAIBB2m8M0E5OOPFfIUx1HsUnNMdsRofAAJmpAACTejhSRrwjedX6S_DOgQ"),
("نظري 3","BQACAgIAAxkBAAIBCGm8M0GOQvKAq1bjdJrUQL5ryPJtAAJnpAACTejhSX6sqUkVBn81OgQ"),
("نظري 4","BQACAgIAAxkBAAIBCWm8M0G7iJUBBqe_xaGLMJTsOooDAAJqpAACTejhSaBH9GUCuRQaOgQ"),
("نظري 5","BQACAgIAAxkBAAIBCmm8M0FtH64uN6fWKtU7AfyaEn47AAJrpAACTejhSaLemAYZBzWEOgQ"),
("نظري 6","BQACAgIAAxkBAAIBC2m8M0E6lr3pETMkCHbZi4-O0RqCAAJtpAACTejhSaMCTu3tekogOgQ"),
("نظري 7","BQACAgIAAxkBAAIBDGm8M0F43plNxAUVmqHTCo3bhvVoAAJ0pAACTejhSfAcDH2GiTbJOgQ"),
("نظري 8","BQACAgIAAxkBAAIBDWm8M0HrnSWUqDN2-2Qh3aWg1PyIAAJ2pAACTejhSSDtlUCkBmLGOgQ"),
("نظري 9","BQACAgIAAxkBAAIBDmm8M0H7sGoGDabBvXta5zJfI-dsAAJ4pAACTejhSaoLTvvsCwHDOgQ"),
("نظري 10","BQACAgIAAxkBAAIBD2m8M0EENq6PMofGlcrJMB5Qd564AAJ8pAACTejhSZFGeKt2ou9aOgQ"),
],

"📚 كميت":[
("نظري 1","BQACAgIAAxkBAAP2abww3UIJ_FhC5lXHEjqgP8gBWGUAAlekAAJN6OFJLX3V2pEJojw6BA"),
("نظري 2","BQACAgIAAxkBAAP3abww3fJ5eJEQVf55hyq7hNPc-jcAAlqkAAJN6OFJiQdAFsLd1tc6BA"),
("نظري 4","BQACAgIAAxkBAAP4abww3dqCYIPtIUWKQid0TKt11bwAAl2kAAJN6OFJFgsN4qccBSg6BA"),
("نظري 5","BQACAgIAAxkBAAP5abww3RD81vfKQMlRUZtIfi72rT0AAl6kAAJN6OFJIIzHJ9M3g2s6BA"),
("نظري 6","BQACAgIAAxkBAAP6abww3da1J-LacmoN1Wash_O_4EgAAl-kAAJN6OFJ-Ew4y6HMv4o6BA"),
("تتمة 3","BQACAgIAAxkBAAP7abww3Z-hYrwbu4uBoq5jUBDFY4YAAmCkAAJN6OFJjWGIOrQAAdoxOgQ"),
]
}

},
"💻 بنيان الحاسوب":{

"📄 النظري":{
"📚 غيت":[
("نظري 1","BQACAgIAAxkBAAPSabwuJ_6-XdYGWxlFibFfMwzyBe8AAiakAAJN6OFJfEBbtgxqty86BA"),
("نظري 2","BQACAgIAAxkBAAPTabwuJ0GDh6z_zCTtSU4nMU_LOqgAAiikAAJN6OFJd1jYecCAd-Q6BA"),
("نظري 3","BQACAgIAAxkBAAPUabwuJ5LDIyKVlG4W94KJFO8g1hEAAiqkAAJN6OFJOq1925tuB306BA"),
("نظري 4","BQACAgIAAxkBAAPVabwuJ75U94V9XiiIe6n1-y7Qz2cAAiykAAJN6OFJC6tlbFvloo06BA"),
("نظري 5","BQACAgIAAxkBAAPWabwuJwF5Zi6vdBt9Xrcu3WT9we0AAi6kAAJN6OFJfT7z5aiMIlU6BA"),
("نظري 6","BQACAgIAAxkBAAPXabwuJ6WpN75a6uhB85cjgr31wHIAAi-kAAJN6OFJLHLBTv4nvIM6BA"),
],

"📚 كميت":[
("نظري 1","BQACAgIAAxkBAAPJabwtriFBTF6nMvvbuG-7u7EiYHMAAhmkAAJN6OFJB1DellaOQfs6BA"),
("نظري 2","BQACAgIAAxkBAAPKabwtrlGrYJu1CS446WR59otmgCQAAh-kAAJN6OFJwQHnU_sOyrY6BA"),
("نظري 3","BQACAgIAAxkBAAPLabwtrmZUDp3BQcbZfeRlQ2lZm18AAiKkAAJN6OFJght-IZpRnnY6BA"),
("نظري 4","BQACAgIAAxkBAAPMabwtrlMhv63PDLYYk-f8X0P25ZkAAiOkAAJN6OFJTUDTbpN2WSE6BA"),
]
},

"🧪 العملي":{
"📚 غيت":[
("عملي 1","BQACAgIAAxkBAAPeabwvFsF3cf3Q1GGwChZuE_whk7UAAjGkAAJN6OFJSVY2B5DtHmA6BA"),
("عملي 2","BQACAgIAAxkBAAPfabwvFmjeanU9ph6HozbJHjNLNMwAAjKkAAJN6OFJZpgqhlnAS-E6BA"),
("عملي 3","BQACAgIAAxkBAAPgabwvFjyLkvVkqF2sJlPU3UaUhkYAAjakAAJN6OFJWQP-KeLZM_46BA"),
("عملي 4","BQACAgIAAxkBAAPhabwvFiqrzZk61NXumCYTbxoGaxIAAjekAAJN6OFJz9lFwbEItZ46BA"),
("عملي 5","BQACAgIAAxkBAAPiabwvFgGa5K4O82qt6aj7VBGRVAQAAjqkAAJN6OFJwvzov3NPHGA6BA"),
("عملي 6","BQACAgIAAxkBAAPjabwvFj8ejgf3SlZYAAHDRr3QEqN3AAI-pAACTejhSerkhTEznWVpOgQ"),
],

"📚 كميت":[
("عملي 1+2","BQACAgIAAxkBAAPrabwv8CrI0uL2zosGAAF0it2NDghGAAJApAACTejhSYGAMHY214ewOgQ"),
("عملي 3+4","BQACAgIAAxkBAAPsabwv8GDZowL1KCcMirz0iz0chusAAkSkAAJN6OFJoiOPFROB08k6BA"),
("عملي 5","BQACAgIAAxkBAAPtabwv8KWRGH6qOR4uvqVp2o-4kk0AAkekAAJN6OFJlTxWmMfIElw6BA"),
("عملي 6","BQACAgIAAxkBAAPuabwv8Ao9Xj3TVFp6lOsGcwABrx8sAAJQpAACTejhSUswLC7IsDz6OgQ"),
("تتمة","BQACAgIAAxkBAAP0abww3QABePjNjhTQpjIpfTeUZP6TAAJSpAACTejhSSfcRtyRO1enOgQ"),
("دورات","BQACAgIAAxkBAAP1abww3Q3VmFcNBihXnvJSQzE0CLgAAlOkAAJN6OFJOj6OiUlcGdA6BA"),
]
}

},

}
}
}
# --- الدوال المساعدة ---

def kb(options, back=True):
    opts = list(options)
    rows = [opts[i:i+2] for i in range(0, len(opts), 2)]
    if back:
        rows.append(["⬅️ رجوع", "🏠 الرئيسية"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def get_node(path):
    node = DATA
    for p in path:
        if isinstance(node, dict) and p in node:
            node = node[p]
        else:
            return DATA
    return node

async def check_sub(user_id, context):
    """التحقق من الاشتراك في القناة"""
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# --- معالجات الأوامر ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_path[uid] = []
    
    # رسالة الترحيب
    welcome_text = (
        "🌹 دعوة في ظهر الغيب هي كل ما نرجوه.\n\n"
        "الغاية من هذا البوت هي تسهيل وصولكم للملفات الأكاديمية بسرعة ويسر.\n\n"
        "📢 يرجى الاشتراك في قناة الدفعة لمتابعة التحديثات:\n"
        "👉 https://t.me/It_2028"
    )

    if not await check_sub(uid, context):
        await update.message.reply_text(f"⚠️ يجب عليك الاشتراك في القناة أولاً:\n{CHANNEL_ID}")
        return

    await update.message.reply_text(welcome_text, reply_markup=kb(DATA.keys(), False))

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    
    # قفل الاشتراك الإجباري
    if not await check_sub(uid, context):
        await update.message.reply_text(f"⚠️ عذراً، يجب الاشتراك في القناة أولاً لتتمكن من استخدام البوت:\n{CHANNEL_ID}")
        return

    if uid not in user_path:
        user_path[uid] = []
    
    path = user_path[uid]

    if text == "🏠 الرئيسية":
        user_path[uid] = []
        await update.message.reply_text("الرئيسية", reply_markup=kb(DATA.keys(), False))
        return

    if text == "⬅️ رجوع":
        if path: path.pop()
        node = get_node(path)
        await update.message.reply_text("رجوع", reply_markup=kb(node.keys(), len(path) != 0))
        return

    node = get_node(path)

    if isinstance(node, dict):
        if text in node:
            path.append(text)
            new_node = node[text]
            if isinstance(new_node, list):
                await update.message.reply_text("اختر الملف:", reply_markup=kb([n for n, _ in new_node]))
            else:
                await update.message.reply_text(f"تم اختيار {text}:", reply_markup=kb(new_node.keys()))
        else:
            await update.message.reply_text("يرجى الاختيار من الأزرار.")

    elif isinstance(node, list):
        file_id = next((f for n, f in node if text == n), None)
        if file_id:
            await update.message.reply_document(file_id)
        else:
            await update.message.reply_text("الملف غير موجود.")

    user_path[uid] = path

if __name__ == "__main__":
    if not TOKEN:
        print("Error: No TOKEN found!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
        print("--- BOT IS RUNNING ---")
        app.run_polling()
