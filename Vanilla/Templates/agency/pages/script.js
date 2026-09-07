
        document.addEventListener('DOMContentLoaded', () => {

            // 1. Mobile Navigation Menu
            const menuToggle = document.querySelector('.ds-menu-toggle');
            const navList = document.getElementById('ds-nav-list');

            if (menuToggle && navList) {
                menuToggle.addEventListener('click', () => {
                    const isOpen = navList.classList.toggle('ds-open');
                    menuToggle.setAttribute('aria-expanded', isOpen);
                    menuToggle.textContent = isOpen ? '✕' : '☰';
                });

                document.querySelectorAll('.ds-nav ul a').forEach(link => {
                    link.addEventListener('click', () => {
                        navList.classList.remove('ds-open');
                        menuToggle.setAttribute('aria-expanded', 'false');
                        menuToggle.textContent = '☰';
                    });
                });
            }

            // 2. Scroll Reveal Animations
            const revealElements = document.querySelectorAll('.ds-reveal');
            const revealObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('ds-visible');
                        revealObserver.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.15,
                rootMargin: "0px 0px -50px 0px"
            });

            revealElements.forEach(el => revealObserver.observe(el));

            // 3. Active Navigation State (Scroll Spy)
            const sections = document.querySelectorAll('section[id]');
            const navLinks = document.querySelectorAll('.ds-nav ul a');

            const navObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const currentId = entry.target.id;
                        navLinks.forEach(link => {
                            const isActive = link.getAttribute('href') === `#${currentId}`;
                            link.classList.toggle('active', isActive);
                            if (isActive) {
                                link.setAttribute('aria-current', 'location');
                            } else {
                                link.removeAttribute('aria-current');
                            }
                        });
                    }
                });
            }, { threshold: 0.4 });

            sections.forEach(section => navObserver.observe(section));
        });
    