$(document).ready(function () {
  $('#equipos').DataTable({
      order: [[1, 'desc']],
      language: {
          lengthMenu: 'Elementos por página _MENU_ ',
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
                    <td>
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