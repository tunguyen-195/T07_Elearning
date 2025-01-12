// static/js/meeting.js
document.getElementById('joinMeetingBtn').onclick = function() {
    const slug = document.getElementById('meetingSlug').value.trim();
    if (slug) {
        window.location.href = meetingRoomUrl.replace('SLUG_PLACEHOLDER', slug);
    } else {
        alert('Vui lòng nhập mã cuộc họp.');
    }
};