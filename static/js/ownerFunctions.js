function editOwner(buttonClicked, isOwned){
    checkbox = buttonClicked.parent()
    row = buttonClicked.parent().parent()
    const url = window.location.pathname
    $.ajax({
        method: isOwned ? 'DELETE' : 'PUT',
        url: url,
        contentType: 'application/json',
        data: JSON.stringify({'machine_id': row[0].id, 'owned': isOwned}),
        beforeSend: function () {
          buttonClicked.html('<svg class="grayIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M304 48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zm0 416c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM48 304c26.5 0 48-21.5 48-48s-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48zm464-48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM142.9 437c18.7-18.7 18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zm0-294.2c18.7-18.7 18.7-49.1 0-67.9S93.7 56.2 75 75s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zM369.1 437c18.7 18.7 49.1 18.7 67.9 0s18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9z"/></svg>')
        }
      }).done(function (response) {
        if (response['code'] == 0) {
          checkbox.html(`<input type="checkbox" class="isOwned" ` + ((response['isOwned'] == 1) ? "checked" : "") + ` onclick="editOwner($(this), ` + response['isOwned'] + `)"/>` + response['isOwned']  + ``)         
        } else {
          alert(response['message'])
        }
      })
}