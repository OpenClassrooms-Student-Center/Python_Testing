let form = document.getElementById("booking-form")
let places_required_input = document.getElementById("places_required_input")
let club_points = Number.parseInt(document.getElementById("club_points").value)
let competition_places = Number.parseInt(document.getElementById("competition_places").value)

let error_displayer = new ErrorDisplayer(form)

places_required_input.addEventListener("input", function(e) {
    let places_required = e.target.value
    if (places_required > 12) {
        error_displayer.add("12", "You can't reserve more than 12 places.")
        e.target.value = 12
    } else if (places_required > club_points) {
        error_displayer.add("club", "Club has not enough points.")
        e.target.value = club_points
    } else if (places_required > competition_places) {
        error_displayer.add("compet", "Competitions has not enough places.")
        e.target.value = competition_places
    } else if (places_required <= 0) {
        e.target.value = 1
    } else {
        error_displayer.clear()
    }
})