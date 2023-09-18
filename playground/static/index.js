// 
// 
//

// Sidebar

const menuItems = document.querySelectorAll(".menu-item");
const currentPage = document.querySelector('body').id;

const changeActiveMenuItems = () => {
    menuItems.forEach((item) => {
        item.classList.remove("active");
        if (item.id === window.location.pathname) {
            item.classList.add("active");
        }
    });
}

let dropdown = false;
menuItems.forEach((item) => {
    item.addEventListener("click", () => {
        if (item.id === 'analytics/') {
            return;
        }
        changeActiveMenuItems();
        item.classList.add("active");
        if (item.id != "settings" || dropdown == true) {
            document.querySelector('.settings-dropdown').style.display = "none";
            dropdown = (false);
            if (item.id === window.location.pathname || item.id == "settings"){
                changeActiveMenuItems();
            }
            else{
            location.replace("https://localhost:8000/" + item.id);
            }
        }
        else{
            document.querySelector('.settings-dropdown').style.display = "flex";
            dropdown = (true);
        }
    })
})

changeActiveMenuItems();

  


// Home Page Photo Grid

var currentIMG = document.getElementById("current-img");
var currentOD = document.getElementById("current-object-detected-image");
var currentImageID = null;
var loaded = Boolean(false);
var lastImageID = null;
const currentPhoto = document.querySelectorAll(".column img");


currentPhoto.forEach((photo) => {
    photo.addEventListener("click", () => {
        currentIMG.innerHTML = "<img src=" + photo.src + "></img>";
        document.querySelector(".photo-selector").style.display = "flex";
        var parts = (photo.src).split("/");
        currentImageID = parts[parts.length - 1];
        $.ajax({
            url: '',
            data: { current_image_id : currentImageID },
            success: function(data) {
                var path = 'playground/static/media/cached/' + currentImageID
                location.href = '/analytics/';
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('Error:', textStatus, errorThrown);
            }
        });
    })
})

currentPhoto.forEach((photo) => {
    photo.addEventListener("mouseover", () => {
        var parts = photo.src.split("/");
        var currentImageID = parts[parts.length - 1];
        console.log(currentImageID);

        $.ajax({
            url: "/get_metrics/",
            method: "POST",
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            data: { current_image_id: currentImageID },
            success: function(data) {
                $('#likes').text(data.likes);
                $('#comments').text(data.comments);
                $('#engagement').text(data.engagement);
                console.log(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("Error:", textStatus, errorThrown);
            }
        });
    });
});









/*

const flipPhoto = document.querySelector(".photo-selector-inner");
flipPhoto.onclick = function(e){
    if (isFlipped == false){
        document.querySelector(".photo-selector-face").style.display = "none";
        document.querySelector(".photo-selector-information").style.display = "flex";
        isFlipped = (true);

        currentOD.innerHTML = "<img src=playground/static/media/cached/" + currentImageID + "></img>";

        console.log("flipped to back");
    }
    else{
        document.querySelector(".photo-selector-information").style.display = "none";
        document.querySelector(".photo-selector-face").style.display = "flex";
        isFlipped = (false);
        console.log("flipped to front");
    }

}

            <div class="photo-selector-information">

                <div class="information-box">

                    <div class="object-id-photo" id="current-object-detected-image">
                    </div>

                    <div class=" informartion">
                        <h1>Object Identification</h1>
                        <h2>Lorem ipsum dolor sit amet. Ex vitae laboriosam At voluptates aperiam quo maxime recusandae
                            aut
                            esse esse et rerum dolore qui autem repellat. Eos corporis sunt in nisi inventore et enim
                            dolorem rem sequi dolorem. Sed animi similique est mollitia doloribus et accusantium
                            necessitatibus. Ex neque minus id velit voluptatem sit quia omnis qui magni vero et fugit
                            blanditiis qui dolor excepturi!
                        </h2>
                    </div>
                </div>

                <div class="information-box">

                    <div class="infomartion">
                        <h1>Sentiment Analysis</h1>
                        <h2>Lorem ipsum dolor sit amet. Ex vitae laboriosam At voluptates aperiam quo maxime recusandae
                            aut
                            esse et rerum dolore qui autem repellat. Eos corporis sunt in nisi inventore et enim
                            dolorem rem sequi dolorem. Sed animi similique est mollitia doloribus et accusantium
                            necessitatibus. Ex neque minus id velit voluptatem sit quia omnis qui magni vero et fugit
                            blanditiis qui dolor excepturi!
                        </h2>
                    </div>

                    <div class="comment-selector">
                        <a>Comments Here</a>
                    </div>
                </div>

            </div>


fetch('../json/id_shortcodes.json')
            .then(function (response) {
                return response.json();
            })
            .then(function (shortcode) {
                appendData(shortcode);
            })
            .catch(function (err) {
                console.log('error: ' + err);
            });
        function appendData(shortcode) {
            var mainContainer = document.getElementById("1");
            for (var i = 0; i < shortcode.length; i++) {
                var div = document.createElement("img");
                div.innerHTML = "/" + shortcode[i][0] + ".jpg";
                mainContainer.appendChild(div);
            }
        }


                $.ajax({
            url: '/home/',
            data: { current_image_id: currentImageID },
            success: function(data) {
                console.log('Success:', data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('Error:', textStatus, errorThrown);
            }
        });



        */