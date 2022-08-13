function getIdValue(clicked_id)
  {
     let a = clicked_id;
      console.log(clicked_id);
      const request = new XMLHttpRequest()
      request.open('POST',`/passengerInfo/${JSON.stringify(a)}`)
      request.send();
      
  }
// function getIdValue(id){
//   const payload = {id:id} 
//   fetch("full link", {
//         method: "POST",
//         headers: {
//           "Accept": "appliation/json",
//           "Content-type": "appliation/json",
//         },
//         body: JSON.stringify(payload),
//       })
//   .then((response) => response.json())
//   .then(
//     (data) => console.log(data)/* proccess you data here*/ ,
//     (error) => {
//       console.error(error);
//     }
//   );
// }
