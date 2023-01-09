function addMachine() {
  console.log($('table > tbody > tr').length)
  $('#add').html(`
                    <td>
                      <input class="form-control" type="text" name="name">
                    </td>
                    <td>
                      <input class="form-control" type="text" name="mac">
                    </td>
                    <td>
                      <input class="form-control" type="text" name="ip">
                    </td>
                    <td class="text-center">
                    <a href="#" onclick="delMachine($(this),false)"><svg class="trashIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z" /></svg></a>
                    </td>
                    <td class="text-center">
                      <a href="#" onclick="saveMachine($(this), false)">GUARDAR</a>
                    </td>
                  `);
  $('tr#add').attr('id', `new_row${$('table > tbody > tr').length}`);
  $('table > tbody').append(`
                                <tr id="add">
                                  <td>
                                  </td>
                                  <td>
                                    <a href="#" onclick="addMachine()"><svg class="plusIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"/></svg></a>
                                  </td>
                                  <td>
                                  </td>
                                  <td>
                                  </td>
                                  <td>
                                  </td>
                                </tr>
                            `);
}

function delMachine(buttonClicked) {
  row = buttonClicked.parent().parent()
  $.ajax({
    method: 'DELETE',
    url: '/edit',
    contentType: 'application/json',
    data: JSON.stringify({"id":row[0].id}),
    beforeSend: function () {
      buttonClicked.html('<svg class="grayIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M304 48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zm0 416c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM48 304c26.5 0 48-21.5 48-48s-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48zm464-48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM142.9 437c18.7-18.7 18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zm0-294.2c18.7-18.7 18.7-49.1 0-67.9S93.7 56.2 75 75s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zM369.1 437c18.7 18.7 49.1 18.7 67.9 0s18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9z"/></svg>')
    }
  }).done(function (response) {
    response ? row.delete() : buttonClicked.html("Error")
  })
}

function editMachine(buttonClicked) {
  row = buttonClicked.parent().parent()

  
}

function saveMachine(buttonClicked, exists) {
  row = buttonClicked.parent().parent()

  machine = {
    "id": exists ? row[0].id : "",
    "name": $(row).find('input[name="name"]').val(),
    "mac": $(row).find('input[name="mac"]').val(),
    "ip": $(row).find('input[name="ip"]').val()
  }
  $.ajax({
    method: exists ? 'POST' : 'PUT',
    url: '/edit',
    contentType: 'application/json',
    data: JSON.stringify(machine),
    beforeSend: function () {
      buttonClicked.html('<svg class="grayIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M304 48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zm0 416c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM48 304c26.5 0 48-21.5 48-48s-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48zm464-48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM142.9 437c18.7-18.7 18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zm0-294.2c18.7-18.7 18.7-49.1 0-67.9S93.7 56.2 75 75s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zM369.1 437c18.7 18.7 49.1 18.7 67.9 0s18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9z"/></svg>')
    }
  }).done(function (data) {
    buttonClicked.html(data)
  })
}