class CustomNav extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.innerHTML = `
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
			<div class="container-fluid">
				<a class="navbar-brand" href="#">FaveBinge <i class="fa-solid fa-tv"></i></a>

				<button class="navbar-toggler" type="button" data-bs-toggle="collapse"
					data-bs-target="#mainNav"
					aria-controls="mainNav" aria-expanded="false"
					aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>

				<div class="collapse navbar-collapse" id="mainNav">
					<ul class="navbar-nav me-auto mb-2 mb-lg-0">
						<li class="nav-item">
							<a class="nav-link" href="./index.html">Home</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="./about.html">About</a>
						</li>
					</ul>
					<a class="d-flex me-2 btn btn-outline-success" href="./login.html">Login</a>
					<a class="d-flex me-2 btn btn-outline-success" href="./register.html">Register</a>
				</div>
			</div>
		</nav>
    `;
  }
}

class CustomFooter extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.innerHTML = `
      <footer class="container text-center">
			<p>Author: Ishani Kathuria</p>
			<p>
				||
				<a href="https://linkedin.com/in/ishani-kathuria/" target="_blank">
					LinkedIn
				</a>
				||
				<a href="https://github.com/ikathuria" target="_blank">
					GitHub
				</a>
				||
				<a href="https://medium.com/@ishani-kathuria" target="_blank">
					Medium
				</a>
				||
			</p>
		</footer>
    `;
  }
}

customElements.define("nav-component", CustomNav);
customElements.define("footer-component", CustomFooter);