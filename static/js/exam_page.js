// ***********************************  Timer  ***********************************

exam_id = document.getElementById('exam_id').value;
console.log(exam_id)

function countdown( elementName, minutes, seconds ){
    var element, endTime, hours, mins, msLeft, time;
    function twoDigits( n )

    {return (n <= 9 ? "0" + n : n);}

    element = document.getElementById( elementName );
    endTime = (+new Date) + 1000 * (60*minutes + seconds) + 500;
    updateTimer();


    function updateTimer()
    {
        msLeft = endTime - (+new Date);

        if ( msLeft < 1000 ) {
            window.location.href = "/student/result/"+exam_id;
        } else {
            time = new Date( msLeft );
            hours = time.getUTCHours();
            mins = time.getUTCMinutes();
            element.innerHTML = (hours ? hours + ':' + twoDigits( mins ) : mins) + ':' + twoDigits( time.getUTCSeconds() );
            setTimeout( updateTimer, time.getUTCMilliseconds() + 500 );
        }
    }
}

countdown( "ten-countdown", 30, 0 );
//  ***********************************  page next and previous  ***********************************

    let currentPage = 1;
    const totalPages = 15;

    function showPage(action, pk) {
      const pages = document.querySelectorAll('.page');

      pages[currentPage - 1].classList.remove('active');

      if (action === 'prev') {
        currentPage = Math.max(currentPage - 1, 1);
      } else if (action === 'next') {

        console.log(pk)

        currentPage = Math.min(currentPage + 1, totalPages);
      }

      pages[currentPage - 1].classList.add('active');
    }

// ***********************************  Answer Submission  ***********************************
    function submitAnswer(a){
      j = document.getElementById("floatingTextarea_"+a).value

      $.ajax({
        type: 'get',
        url: '/student/answer_questions_in_exam/'+a,
        data: {'answer':j},
        success: function(response) {alert(response.msg)}
      })
    }
