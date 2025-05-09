const dragDropArea = document.getElementById('drag-drop-area');
const fileInput = document.getElementById('file-upload');
const uploadedImage = document.getElementById('uploaded-img');
const submitButton = document.getElementById('submit-button');
const form = document.querySelector('form');
const originalUrlInput = document.getElementById('original_url');
const placeholderBox = document.getElementById('placeholder-box');

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
    // remove black border
    dragDropArea.classList.remove('noimage');
    // remove text (if it exists) saying drag and drop by clearing html content within placeholder div 
    try {
        const placeholderBox = document.getElementById('placeholder-box')
        placeholderBox.innerHTML = ""
    } catch {}
    // move upload button to underneath photo
    const element = document.getElementById('moving');
    if (element) {
        const target = document.getElementById('moveto');
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

        // simulate file input for form submission
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        // clear original image URL since new image has been uploaded
        if (originalUrlInput) {
            originalUrlInput.value = "";
        }
    }

    reader.readAsDataURL(file); // read file as data url for image preview
}

// trigger form submission only if file is selected
form.addEventListener('submit', function(event) {
    // no file selected, prevent form submission and prompt user to select image
    if (fileInput.files.length === 0 && originalUrlInput.value === "") {
        event.preventDefault();
        alert("Please select a file before submitting.");
        fileInput.click();
    } else {
        // loading screen
        const image = document.getElementById("pixelated-img");
        image.style.display = 'block';
        image.src = '/static/hourglass.gif';
    }
});