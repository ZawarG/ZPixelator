const dragDropArea = document.getElementById('drag-drop-area');
const fileInput = document.getElementById('file-upload');
const uploadedImage = document.getElementById('uploaded-img');
const submitButton = document.getElementById('submit-button');
const form = document.querySelector('form');
// const placeholderBox = document.getElementById('placeholder-box');

// when something is dragged over drag-drop-area
dragDropArea.addEventListener('dragover', function (event) {
    // prevents browser from preventing drop
    event.preventDefault();
    // changes display of div
    dragDropArea.classList.add('drag-over');
});

// when dragged item leaves drag-drop-area
dragDropArea.addEventListener('dragleave', function () {
    // return div style to original
    dragDropArea.classList.remove('drag-over');
});

// when item is dropped
dragDropArea.addEventListener('drop', function (event) {
    event.preventDefault();
    dragDropArea.classList.remove('drag-over');

    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/JPEG', 'image/JPG', 'image/PNG'];
    // retrieve dropped file
    const files = event.dataTransfer.files;
    
    if (files.length > 0) {
        // check for valid file types
        if (validTypes.includes(files[0].type.toLowerCase())) {
            // update formatting of page
            reformat()

            handleFileUpload(files[0]);
        } else {
            alert('Please upload an image.');
        }
    }
});

function reformat() {
    dragDropArea.classList.remove('noimage');
    const element = document.getElementById('moving');
    if (element) {
        const target = document.getElementById('moveto');
        console.log(element, target)
        target.appendChild(element);
    }
        

}

// handle file upload and display preview of image
function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('image', file);

    const reader = new FileReader();
    reader.onload = function (e) {
        // update uploaded image source (preview)
        uploadedImage.src = e.target.result;

        // show uploadedImage on website
        uploadedImage.style.display = 'block';
        // if (placeholderBox !== null) {
        //     placeholderBox.style.display = 'none';
        // }

        // simulate file input for form submission
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
    }

    reader.readAsDataURL(file); // read file as data url for image preview
}

// trigger form submission only if file is selected
form.addEventListener('submit', function(event) {
    console.log("form submission triggered")
    // no file selected, prevent form submission and promot user to select image
    console.log(fileInput.files.length);
    if (fileInput.files.length === 0) {
        event.preventDefault();
        alert("Please select a file before submitting.");
        fileInput.click();
    } else {
        console.log("File selected, proceeding with form submission.");
    }
});