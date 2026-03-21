const usernameInput = document.getElementById("username");
const usernameError = document.getElementById("usernameError");
const submitBtn = document.getElementById("submitBtn");
const registerForm = document.getElementById("registerForm");

submitBtn.disabled = true;

async function checkUsername() {
  const username = usernameInput.value.trim();

  if (username === "") {
    usernameError.textContent = "";
    submitBtn.disabled = true;
    return false;
  }

  try {
    const response = await fetch(`/check-username?username=${encodeURIComponent(username)}`);
    const data = await response.json();

    if (!data.available) {
      usernameError.textContent = data.message;
      submitBtn.disabled = true;
      return false;
    } else {
      usernameError.textContent = "";
      submitBtn.disabled = false;
      return true;
    }
  } catch (error) {
    usernameError.textContent = "Could not check username right now";
    submitBtn.disabled = true;
    return false;
  }
}

usernameInput.addEventListener("input", checkUsername);

registerForm.addEventListener("submit", async function (event) {
  const valid = await checkUsername();

  if (!valid) {
    event.preventDefault();
  }
});