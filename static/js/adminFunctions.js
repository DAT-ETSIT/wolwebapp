$(document).ready(function () {
  $('#equipos').DataTable({
      order: [[0, 'desc']],
      language: {
          lengthMenu: 'Elementos por página: _MENU_ ',
          zeroRecords: 'No se encuentran resultados',
          info: 'Página _PAGE_ de _PAGES_',
          infoEmpty: 'No se encuentran resultados',
          infoFiltered: '',
          search: 'Buscar:',
          paginate: {
              next: ">",
              previous: "<"
          }
      },
  });
});

function addMachine() {
    console.log($('table > tbody > tr').length)
    $('#add').html(`
                    <td>
                      <input class="form-control" type="text" name="machine[${$('table > tbody > tr').length - 1}][name]">
                    </td>
                    <td>
                      <input class="form-control" type="text" name="machine[${$('table > tbody > tr').length - 1}][mac]">
                    </td>
                    <td>
                      <input class="form-control" type="text" name="machine[${$('table > tbody > tr').length - 1}][ip]">
                    </td>
                    <td class="text-center">
                    <a href="#" onclick="delMachine(${$('table > tbody > tr').length - 1})"><svg class="trashIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z" /></svg></a>
                    </td>
                  `);
    $('tr#add').attr('id', `row_${$('table > tbody > tr').length - 1}`);
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
                                </tr>
                            `);
  }

  function delMachine(id) {
    $('#row_' + id + ' > td > input').val("")
  }