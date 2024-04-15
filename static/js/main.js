let profileBtn = document.getElementById("profileBtn")
let dropDownSortingBtn = document.querySelector("#dropDownSortingBtn")
let dropDownCategoryBtn = document.querySelector("#dropDownCategoryBtn")
let dropDownLangBtn =  document.querySelector("#dropDownLangBtn")

if ( profileBtn && !profileBtn.classList.contains('not_auth') ) {
    profileBtn.onclick = () => {
        document.getElementById("dropDownProfile").classList.toggle("hidden")
    }
}
if (dropDownSortingBtn) {
    dropDownSortingBtn.onclick = () => {
        document.getElementById("dropdownSort").classList.toggle("hidden")
    }
}
if (dropDownCategoryBtn) {
    dropDownCategoryBtn.onclick = () => {
        document.getElementById("dropdownCategory").classList.toggle("hidden")
    }
}
if (dropDownLangBtn) {
    dropDownLangBtn.onclick = () => {
        document.getElementById("dropdownLang").classList.toggle("hidden")
    }
}



document.addEventListener("click", (event) => {
    let dropdownSort = document.getElementById("dropdownSort")
    let dropDownProfile = document.getElementById("dropDownProfile")
    let dropDownCategory = document.getElementById("dropdownCategory")
    let dropdownLang = document.getElementById("dropdownLang")


    if (dropdownSort && dropdownSort.classList.contains('hidden') == false &&  event.target.id !== 'dropDownSortingBtn') {
        dropdownSort.classList.add("hidden")
    } 

    if (dropDownCategory && dropDownCategory.classList.contains('hidden') == false &&  event.target.id !== 'dropDownCategoryBtn') {
        dropDownCategory.classList.add("hidden")
    } 


    if (dropdownLang && dropdownLang.classList.contains('hidden') == false &&  event.target.id !== 'dropDownLangBtn') {
        dropdownLang.classList.add("hidden")
    }     

    if (dropDownProfile && dropDownProfile.classList.contains('hidden') == false &&  !event.target.classList.contains('profileBtn')) {
        dropDownProfile.classList.add("hidden")
    }     

})
