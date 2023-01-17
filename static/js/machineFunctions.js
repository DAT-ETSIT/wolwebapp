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
                    <td>
                      <input class="form-control" type="text" name="port" value=9>
                    </td>
                    <td>
                    </td>
                    <td class="text-center">
                      <a href="#" onclick="cancelMachine($(this))"><svg class="saveIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path d="M310.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L160 210.7 54.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L114.7 256 9.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L160 301.3 265.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L205.3 256 310.6 150.6z"/></svg></a>
                      &nbsp;<a href="#" onclick="saveMachine($(this), false)"><svg class="saveIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M64 32C28.7 32 0 60.7 0 96V416c0 35.3 28.7 64 64 64H384c35.3 0 64-28.7 64-64V173.3c0-17-6.7-33.3-18.7-45.3L352 50.7C340 38.7 323.7 32 306.7 32H64zm0 96c0-17.7 14.3-32 32-32H288c17.7 0 32 14.3 32 32v64c0 17.7-14.3 32-32 32H96c-17.7 0-32-14.3-32-32V128zM224 416c-35.3 0-64-28.7-64-64s28.7-64 64-64s64 28.7 64 64s-28.7 64-64 64z"/></svg></a>
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
                                  <td>
                                  </td>
                                </tr>
                            `);
}

function saveMachine(buttonClicked, exists) {
  row = buttonClicked.parent().parent()

  id = exists ? row[0].id : '';
  machineName = $(row).find('input[name="name"]').val();
  mac = $(row).find('input[name="mac"]').val();
  ip = $(row).find('input[name="ip"]').val();
  port = $(row).find('input[name="port"]').val();

  if (machineName == "") {
    alert("El nombre la máquina no puede estar vacío.");
    return;
  }
  if (mac == "") {
    alert("La dirección MAC de la máquina no puede estar vacía.");
    return;
  }
  if (ip == "") {
    alert("La dirección IP de la máquina no puede estar vacía.");
    return;
  }
  if (port == "") {
    alert("El puerto de la máquina no puede estar vacío.");
    return;
  }

  machine = {
    "id": id,
    "name": machineName,
    "mac": mac,
    "ip": ip,
    "port": port
  }

  $.ajax({
    method: exists ? 'POST' : 'PUT',
    url: exists ? '/machines/' + id : '/machines',
    contentType: 'application/json',
    data: JSON.stringify(machine),
    beforeSend: function () {
      buttonClicked.html('<svg class="grayIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M304 48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zm0 416c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM48 304c26.5 0 48-21.5 48-48s-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48zm464-48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM142.9 437c18.7-18.7 18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zm0-294.2c18.7-18.7 18.7-49.1 0-67.9S93.7 56.2 75 75s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zM369.1 437c18.7 18.7 49.1 18.7 67.9 0s18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9z"/></svg>')
    }
  }).done(function (response) {
    if (response['code'] == 0) {
      if (!exists) row[0].id = response['id']

      $(row).html(`
          <td>
            <p class="name">` + machine['name'] + `</p>
          </td>
          <td>
            <p class="mac">` + machine['mac'] + `</p>
          </td>
          <td>
            <p class="ip">` + machine['ip'] + `</p>
          </td>
          <td>
            <p class="port">` + machine['port'] + `</p>
          </td>
          <td class="text-center"><a href="#" onclick="wakeMachine($(this), '/wol/{{ machine.id }}');"><svg
            class="powerOnIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
            <path
              d="M400 54.1c63 45 104 118.6 104 201.9 0 136.8-110.8 247.7-247.5 248C120 504.3 8.2 393 8 256.4 7.9 173.1 48.9 99.3 111.8 54.2c11.7-8.3 28-4.8 35 7.7L162.6 90c5.9 10.5 3.1 23.8-6.6 31-41.5 30.8-68 79.6-68 134.9-.1 92.3 74.5 168.1 168 168.1 91.6 0 168.6-74.2 168-169.1-.3-51.8-24.7-101.8-68.1-134-9.7-7.2-12.4-20.5-6.5-30.9l15.8-28.1c7-12.4 23.2-16.1 34.8-7.8zM296 264V24c0-13.3-10.7-24-24-24h-32c-13.3 0-24 10.7-24 24v240c0 13.3 10.7 24 24 24h32c13.3 0 24-10.7 24-24z" />
          </svg></a>
            <a href="#" onclick="requestPing($(this), '/ping/{{ machine.id }}');"><svg
                class="icono" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                <path
                  d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256s256-114.6 256-256S397.4 0 256 0zM256 464c-114.7 0-208-93.31-208-208S141.3 48 256 48s208 93.31 208 208S370.7 464 256 464zM256 336c-18 0-32 14-32 32s13.1 32 32 32c17.1 0 32-14 32-32S273.1 336 256 336zM289.1 128h-51.1C199 128 168 159 168 198c0 13 11 24 24 24s24-11 24-24C216 186 225.1 176 237.1 176h51.1C301.1 176 312 186 312 198c0 8-4 14.1-11 18.1L244 251C236 256 232 264 232 272V288c0 13 11 24 24 24S280 301 280 288V286l45.1-28c21-13 34-36 34-60C360 159 329 128 289.1 128z" />
              </svg></a>
          </td>
          <td class="text-center">
            <a href="#" onclick="editMachine($(this))"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit-3"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg></a>
            <a href="#" onclick="delMachine($(this))"><svg class="trashIcon"
                xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                <path
                  d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z" />
              </svg></a>
          </td>
    `)
    } else {
      alert(response['message'])
    } 
  })
}

function delMachine(buttonClicked) {
  row = buttonClicked.parent().parent()
  id = row[0].id
  $.ajax({
    method: 'DELETE',
    url: '/machines/' + id,
    contentType: 'application/json',
    beforeSend: function () {
      buttonClicked.html('<svg class="grayIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M304 48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zm0 416c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM48 304c26.5 0 48-21.5 48-48s-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48zm464-48c0-26.5-21.5-48-48-48s-48 21.5-48 48s21.5 48 48 48s48-21.5 48-48zM142.9 437c18.7-18.7 18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zm0-294.2c18.7-18.7 18.7-49.1 0-67.9S93.7 56.2 75 75s-18.7 49.1 0 67.9s49.1 18.7 67.9 0zM369.1 437c18.7 18.7 49.1 18.7 67.9 0s18.7-49.1 0-67.9s-49.1-18.7-67.9 0s-18.7 49.1 0 67.9z"/></svg>')
    }
  }).done(function (response) {
    response['code'] == 0 ? row.html('') : alert(response['message'])
  })
  
}

function editMachine(buttonClicked) {
  row = buttonClicked.parent().parent()
  machine_name = (row.children()[0].children[0].innerHTML)
  machine_mac = (row.children()[1].children[0].innerHTML)
  machine_ip = (row.children()[2].children[0].innerHTML)
  machine_port = (row.children()[3].children[0].innerHTML)
  localStorage.setItem("machine_"+row[0].id, row.html())
  $(row).html(
    `
    <td>
      <input class="form-control" type="text" name="name" value=` + machine_name + `>
    </td>
    <td>
      <input class="form-control" type="text" name="mac" value=` + machine_mac + `>
    </td>
    <td>
      <input class="form-control" type="text" name="ip" value=` + machine_ip + `>
    </td>
    <td>
      <input class="form-control" type="text" name="port" value=` + machine_port + `>
    </td>
    <td>
    </td>
    <td class="text-center">
      <a href="#" onclick="cancelMachine($(this))"><svg class="saveIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path d="M310.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L160 210.7 54.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L114.7 256 9.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L160 301.3 265.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L205.3 256 310.6 150.6z"/></svg></a>
      &nbsp;<a href="#" onclick="saveMachine($(this), true)"><svg class="saveIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M64 32C28.7 32 0 60.7 0 96V416c0 35.3 28.7 64 64 64H384c35.3 0 64-28.7 64-64V173.3c0-17-6.7-33.3-18.7-45.3L352 50.7C340 38.7 323.7 32 306.7 32H64zm0 96c0-17.7 14.3-32 32-32H288c17.7 0 32 14.3 32 32v64c0 17.7-14.3 32-32 32H96c-17.7 0-32-14.3-32-32V128zM224 416c-35.3 0-64-28.7-64-64s28.7-64 64-64s64 28.7 64 64s-28.7 64-64 64z"/></svg></a>
    </td>
  `)
}

function cancelMachine(buttonClicked){
  row = buttonClicked.parent().parent()
  prevRow=localStorage.getItem("machine_"+row[0].id)
  localStorage.removeItem("machine_"+row[0].id)
  $(row).html(prevRow)
}