
// This is navbar toggle arrow <<
const closeToggleBtn = document.getElementById("closeToggleBtn");
const leftSideBar = document.getElementById("leftSideBar");
const mainContent = document.getElementById("main-content");
const navbarHeading = document.getElementById("navbarHeading");
var hamburger = document.getElementById("hamburger");

// Function to close the sidebar
function closeSidebar() {
leftSideBar.classList.remove("left-sidebar-open");

}

closeToggleBtn.addEventListener("click", () => {
leftSideBar.classList.toggle("left-400");
mainContent.classList.toggle("left-0");
navbarHeading.classList.toggle("left-0");
closeToggleBtn.classList.toggle("left-sidebar-toggle-turn");
});

// Show userProfile drop-down
const defaultDropdown = document.getElementById("defaultDropdown");
defaultDropdown.addEventListener("click", (event) => {
const showDropDown = document.getElementById("showDropDown");
showDropDown.classList.toggle("show");
event.stopPropagation();

});

document.addEventListener('click', (event) => {
if(!showDropDown.contains(event.target) && !defaultDropdown.contains(event.target) && !hamburger.contains(event.target)){
showDropDown.classList.remove('show')
}

})

// Show side-bar when click on hamburger
hamburger.addEventListener("click", (event) => {
leftSideBar.classList.toggle("left-sidebar-open");
event.stopPropagation();
});

// Close sidebar when clicking anywhere outside of it
document.addEventListener("click", (event) => {
if (!leftSideBar.contains(event.target) && !hamburger.contains(event.target)) {
    leftSideBar.classList.remove("left-sidebar-open");
}
});




//fuction to hide left_side
function hideLeftSidebar() {
    document.querySelector('.left-sidebar').classList.add('d-none');
}

// for convert date string inti desire date formate

function formatDateToYYYYMMDD(inputDateString) {
    const dateObject = new Date(inputDateString);
  
    const year = dateObject.getFullYear();
    const month = (dateObject.getMonth() + 1).toString().padStart(2, '0');
    const day = dateObject.getDate().toString().padStart(2, '0');
  
    return `${year}-${month}-${day}`;
  }

// for popup image preview modal
// const modalImage = document.getElementById('modalImage');
// function openModal(imageUrl) {
//     modalImage.src = imageUrl;
//     console.log('imageUrl ==>>>', imageUrl)
//   }

// function handleFilePreviewAndDownload(filename, imageRoute, fileRoute) {
//     const downloadLink = document.getElementById('downloadLink');
//     // for checking image extension preview
//     const fileExtension = (filename || '').split('.').pop().toLowerCase();
//     const allowedImageExtensions = ['jpg', 'jpeg', 'png', 'gif'];
//     const isImage = allowedImageExtensions.includes(fileExtension);

//     console.log('isImage ===>>>:::::::', isImage);
//     if (isImage) {
//         const fetchUrl = `${imageRoute}${filename}`;
//         console.log('fetchUrl ==>>>', fetchUrl);
//         // Display image preview modal
//         openModal(fetchUrl);
//         $('#imageModal').modal('show');

//         // Hide download link
//         downloadLink.style.display = 'none';
//     } else {
//         const fileDownloadURL = `${fileRoute}${filename}`;
//         console.log('fileDownloadURL ==>>', fileDownloadURL);

//         // Hide image preview modal
//         $('#imageModal').modal('hide');

//         // Create a link element for download
//         downloadLink.href = fileDownloadURL;
//         downloadLink.download = filename;
//         modalImage.src  = '';
//         if (modalImage.parentNode) {
//             modalImage.parentNode.removeChild(modalImage);
//         }
    
//         // Show download link
//         downloadLink.style.display = 'block';
//     }
// }


//  for download file function
function  downloadFile(fileName, fileUrl) {
  console.log("fileName in side public folder ==>>", fileName);
  console.log("file url in side public folder ==>>", fileUrl);
  fetch(fileUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.blob();
    })
    .then((blob) => {
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}


// function fileContainerData(fileArray) {
//     // console.log('fileUrl inside public folder ===>>>', fileUrl);
//   console.log("fileArray inside public folder :::::: ===>>>");
//   //Promise.all to wait for all downloads to finish
//   Promise.all(fileArray)
//     .then((values) => {
//       console.log("All files downloaded successfully", values);
//     })
//     .catch((error) => {
//       console.error("error ::::", error);
//     });
// }

//


// function downloadFiles(fileArray) {
//     const promises = fileArray.map(file => downloadFile(file.fileName, file.fileUrl));
//     return Promise.all(promises)
//         .catch(error => {
//             console.error('There was a problem downloading files:', error);
//             alert('Some files are not available');
//         });
// }


// for download function files
// function handleButtonClick(event) {
//     const button = event.target.closest('button');
//     console.log('button  ===>>', button);
    
//     if (button && button.id && button.classList.contains('download-file')) {
//         const fileName = button.getAttribute('data-filename');
//         console.log('fileName ==>>>', fileName);
        
//         const fileUrl = `<%- BASE_URL %>research/book-publication-main/edited-book-publication/download/${fileName}`;
//         downloadFile(fileName, fileUrl);
//     }
// }

// document.addEventListener('click', handleButtonClick);


// // Get the dropdown icon element
// const dropdownIcon = document.getElementById('dropdown-icon');

// // Add an event listener to toggle the icon class when the dropdown is shown or hidden
// $('#research').on('show.bs.collapse', function () {
//     dropdownIcon.classList.remove('fa-angle-down');
//     dropdownIcon.classList.add('fa-angle-up');
// }).on('hide.bs.collapse', function () {
//     dropdownIcon.classList.remove('fa-angle-up');
//     dropdownIcon.classList.add('fa-angle-down');
// });







  





