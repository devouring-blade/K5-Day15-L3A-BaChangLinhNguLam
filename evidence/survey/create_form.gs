/**
 * Tạo Google Form khảo sát "Đặt đồ ăn qua app".
 * Cách chạy: script.google.com → Dự án mới → dán toàn bộ file này → chọn hàm createSurvey → Chạy.
 * Xem link form ở "Nhật ký thực thi" (Execution log).
 * Bộ câu hỏi giống hệt evidence/survey/questions.md.
 */
function createSurvey() {
  var form = FormApp.create('Đặt đồ ăn qua app: khảo sát 2 phút');
  form.setDescription(
    'Khảo sát ẩn danh, không thu tên, số điện thoại hay email. ' +
    'Phục vụ bài hackathon AI20K. Hỏi về những lần đặt đồ ăn đã xảy ra.');
  form.setCollectEmail(false);
  form.setProgressBar(true);

  // ---- Phần 1: Thói quen ----
  form.addMultipleChoiceItem()
    .setTitle('1. Bạn là:')
    .setChoiceValues(['Sinh viên', 'Đi làm', 'Khác'])
    .setRequired(true);
  var q2 = form.addMultipleChoiceItem()
    .setTitle('2. Bạn hay đặt đồ ăn qua app nào nhất?')
    .setRequired(true);
  var q3 = form.addMultipleChoiceItem()
    .setTitle('3. Trung bình mỗi tuần bạn đặt bao nhiêu đơn đồ ăn qua app?')
    .setRequired(true);

  // ---- Phần 2: 5 đơn gần nhất ----
  form.addPageBreakItem().setTitle('5 đơn gần nhất');
  var q4 = form.addMultipleChoiceItem()
    .setTitle('4. Trong 5 đơn gần nhất, có mấy đơn bị GIAO TRỄ (đến muộn hơn giờ app dự kiến từ 15 phút trở lên)?')
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('5. Trong 5 đơn gần nhất, có mấy đơn bị THIẾU hoặc SAI MÓN?')
    .setChoiceValues(['0', '1', '2', '3', '4', '5', 'Không nhớ'])
    .setRequired(true);

  // ---- Phần 3: Lần giao trễ gần nhất ----
  form.addPageBreakItem().setTitle('Lần giao trễ gần nhất');
  form.addMultipleChoiceItem()
    .setTitle('6. Lần giao trễ gần nhất, đơn đến muộn khoảng bao lâu so với dự kiến?')
    .setChoiceValues(['15–30 phút', '30–60 phút', 'Trên 60 phút', 'Không nhớ'])
    .setRequired(true);
  form.addCheckboxItem()
    .setTitle('7. Lúc đó bạn đã làm gì? (chọn nhiều)')
    .setChoiceValues(['Khiếu nại trong app', 'Nhắn/gọi shipper', 'Nhắn/gọi quán', 'Huỷ đơn', 'Bỏ qua, chờ tiếp'])
    .showOtherOption(true)
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('8. Bạn có được bù gì không?')
    .setChoiceValues(['Voucher', 'Hoàn tiền một phần', 'Hoàn tiền toàn bộ', 'Không được gì', 'Không khiếu nại nên không biết'])
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('9. Nếu đã khiếu nại: mất bao lâu từ lúc khiếu nại đến khi có kết quả?')
    .setChoiceValues(['Dưới 5 phút', '5–30 phút', 'Vài giờ', 'Hơn 1 ngày', 'Không có kết quả', 'Không khiếu nại'])
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('10. Nếu không khiếu nại, vì sao?')
    .setChoiceValues(['Không biết có được bù không', 'Khiếu nại mất công quá', 'Nghĩ khiếu nại cũng không được gì', 'Không bực đến mức đó'])
    .showOtherOption(true)
    .setRequired(false);

  // ---- Phần 4: Kể lại ----
  var p4 = form.addPageBreakItem().setTitle('Kể lại');
  form.addParagraphTextItem()
    .setTitle('11. Kể ngắn lần gần nhất đơn đồ ăn của bạn có vấn đề (trễ, thiếu món…): chuyện gì xảy ra, bạn làm gì, khó chịu nhất ở đâu?')
    .setHelpText('Không ghi tên quán, tên người, số điện thoại.')
    .setRequired(false);

  // ---- Rẽ nhánh ----
  var GO = FormApp.PageNavigationType.CONTINUE;
  var END = FormApp.PageNavigationType.SUBMIT;
  q2.setChoices([
    q2.createChoice('ShopeeFood', GO),
    q2.createChoice('GrabFood', GO),
    q2.createChoice('BeFood', GO),
    q2.createChoice('Xanh SM Ngon', GO),
    q2.createChoice('App khác', GO),
    q2.createChoice('Không đặt đồ ăn qua app', END)
  ]);
  q3.setChoices([
    q3.createChoice('0', END),
    q3.createChoice('1–2', GO),
    q3.createChoice('3–5', GO),
    q3.createChoice('6–10', GO),
    q3.createChoice('Trên 10', GO)
  ]);
  q4.setChoices([
    q4.createChoice('0', p4),          // không bị trễ lần nào → bỏ qua phần 3
    q4.createChoice('1', GO),
    q4.createChoice('2', GO),
    q4.createChoice('3', GO),
    q4.createChoice('4', GO),
    q4.createChoice('5', GO),
    q4.createChoice('Không nhớ', GO)
  ]);

  Logger.log('Link gửi người trả lời: ' + form.getPublishedUrl());
  Logger.log('Link chỉnh sửa (giữ riêng): ' + form.getEditUrl());
}
