function addUser() {
  $('#add').html(`
                    <td>
                      <input class="form-control" type="text" name="email">
                    </td>
                    <td> 
                    </td>
                    <td> 
                    </td>
                    <td class="text-center">
                      <a href="#" onclick="cancelUser($(this))">CANCELAR</a>
                      <a href="#" onclick="saveUser($(this))">GUARDAR</a>
                    </td>
                  `);
  $('tr#add').attr('id', `new_row${$('table > tbody > tr').length}`);
  $('table > tbody').append(`
                                <tr id="add">
                                  <td>
                                  </td>
                                  <td>
                                    <a href="#" onclick="addUser()"><svg class="plusIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"/></svg></a>
                                  </td>
                                  <td>
                                  </td>
                                  <td>
                                  </td>
                                </tr>
                            `);
}

function saveUser(buttonClicked){
  row = buttonClicked.parent().parent()
  email = $(row).find('input[name="email"]').val();

  if (email == "") {
    alert("El correo del usuario no puede estar vacío.");
    return;
  }

  user = {
    "email": email
  }

  $.ajax({
    method: 'PUT',
    url: '/users',
    contentType: 'application/json',
    data: JSON.stringify(user),
    beforeSend: function () {
      buttonClicked.html('<svg class="grayIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M304 48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zm0 416c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM48 304c26.5 0 48-21.5 48-48s-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48zm464-48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM142.9 437c18.7-18.7 18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zm0-294.2c18.7-18.7 18.7-49.1 0-67.9S93.7 56.2 75 75s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zM369.1 437c18.7 18.7 49.1 18.7 67.9 0s18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9z"/></svg>')
    }
  }).done(function (response) {
      if(response['code'] == 0) {
        row[0].id = response['id']
        $(row).html(`
            <td class="text-center">
              <p class="name">` + user['email'] + `</p>
            </td>
            <td class="text-center">
              <input type="checkbox" class="isAdmin" onclick="editUser($(this), 0)" >0
            </td>
            <td class="text-center">
              <a class="pass" onclick="restorePass()">RESTAURAR CONTRASEÑA</a>
            </td>
            <td class="text-center">
            <a href="#" onclick=""><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-monitor"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg></a>
            <a href="#" onclick="delUser($(this))"><svg class="trashIcon"
                  xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                  <path
                    d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z" />
                </svg></a>
            </td>
        `);
      } else {
        alert(response['message']);
      }
  })
}

function editUser(buttonClicked, isAdmin){
    checkbox = buttonClicked.parent()
    row = buttonClicked.parent().parent()
    $.ajax({
        method: 'POST',
        url: '/users',
        contentType: 'application/json',
        data: JSON.stringify({'id': row[0].id, 'admin': isAdmin}),
        beforeSend: function () {
          buttonClicked.html('<svg class="grayIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M304 48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zm0 416c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM48 304c26.5 0 48-21.5 48-48s-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48zm464-48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM142.9 437c18.7-18.7 18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zm0-294.2c18.7-18.7 18.7-49.1 0-67.9S93.7 56.2 75 75s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zM369.1 437c18.7 18.7 49.1 18.7 67.9 0s18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9z"/></svg>')
        }
      }).done(function (response) {
        if (response['code'] == 0) {
          checkbox.html(`<input type="checkbox" class="isAdmin" ` + ((response['isAdmin'] == 1) ? "checked" : "") + ` onclick="editUser($(this), ` + response['isAdmin'] + `)"/>` + response['isAdmin']  + ``)         
        } else {
          alert(response['message'])
        }
      })
}

function restorePass(buttonClicked) {

}

function cancelUser(buttonClicked){
  row = buttonClicked.parent().parent()
  row.html('')
}

function delUser(buttonClicked){
  row = buttonClicked.parent().parent()
  $.ajax({
    method: 'DELETE',
    url: '/users',
    contentType: 'application/json',
    data: JSON.stringify({'id': row[0].id}),
    beforeSend: function () {
      buttonClicked.html('<svg class="grayIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M304 48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zm0 416c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM48 304c26.5 0 48-21.5 48-48s-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48zm464-48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM142.9 437c18.7-18.7 18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zm0-294.2c18.7-18.7 18.7-49.1 0-67.9S93.7 56.2 75 75s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zM369.1 437c18.7 18.7 49.1 18.7 67.9 0s18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9z"/></svg>')
    }
  }).done(function (response) {
    if (response['code'] == 0) {
      row.html('')
    } else {
      buttonClicked.html("Error")
      alert(response['message'])
    }
  })
}