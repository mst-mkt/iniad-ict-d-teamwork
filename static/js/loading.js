let isLoading = false;

const activateLoading = () => {
  if (isLoading) {
    return;
  }

  isLoading = true;
  const loading = document.getElementById("loading");
  loading.classList.add("active");
};

const deactivateLoading = () => {
  if (!isLoading) {
    return;
  }

  isLoading = false;
  const loading = document.getElementById("loading");
  loading.classList.remove("active");
};

window.addEventListener("load", () => {
  const callLoading = document.getElementById("call_loading");
  callLoading.addEventListener("click", () => {
    activateLoading();
  });
});
