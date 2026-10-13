/**
 * script.js — Client-side enhancements for AquaWatch
 * Smart Water Monitoring and Complaint Management System
 */

/* ─── Navbar Mobile Toggle ──────────────────────────────────────── */
(function () {
    const toggle = document.getElementById('navToggle');
    const links  = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', function () {
            links.classList.toggle('open');
        });
    }
})();

/* ─── Flash Message Auto-Dismiss ───────────────────────────────── */
(function () {
    setTimeout(function () {
        document.querySelectorAll('.flash').forEach(function (el) {
            el.style.transition = 'opacity 0.5s ease';
            el.style.opacity = '0';
            setTimeout(function () { el.remove(); }, 500);
        });
    }, 5000);
})();

/* ─── Complaint Form — Character Counter ───────────────────────── */
(function () {
    const desc  = document.getElementById('description');
    const count = document.getElementById('charCount');
    if (desc && count) {
        count.textContent = desc.value.length;
        desc.addEventListener('input', function () {
            count.textContent = this.value.length;
            count.style.color = this.value.length < 10
                ? '#c62828'
                : this.value.length > 900
                    ? '#f57f17'
                    : '#94a3b8';
        });
    }
})();

/* ─── Complaint Form — Client-side Validation ──────────────────── */
(function () {
    const form = document.getElementById('complaintForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        let valid = true;
        const errors = [];

        const type = form.querySelector('#complaint_type');
        const loc  = form.querySelector('#location');
        const desc = form.querySelector('#description');
        const prio = form.querySelectorAll('input[name="priority"]');

        if (!type || !type.value) {
            errors.push('Please select a complaint category.');
            valid = false;
        }
        if (!loc || loc.value.trim().length < 5) {
            errors.push('Location must be at least 5 characters.');
            valid = false;
        }
        if (!desc || desc.value.trim().length < 10) {
            errors.push('Description must be at least 10 characters.');
            valid = false;
        }
        const checked = Array.from(prio).some(r => r.checked);
        if (!checked) {
            errors.push('Please select a priority level.');
            valid = false;
        }

        if (!valid) {
            e.preventDefault();
            // Remove old client error box
            const old = document.getElementById('jsErrorBox');
            if (old) old.remove();

            const box = document.createElement('div');
            box.id = 'jsErrorBox';
            box.className = 'error-box';
            box.innerHTML = '<strong>⚠️ Please fix the following:</strong><ul>'
                + errors.map(function (err) { return '<li>' + err + '</li>'; }).join('')
                + '</ul>';
            form.prepend(box);
            box.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            // Disable submit button to prevent double submission
            const btn = document.getElementById('submitBtn');
            if (btn) {
                btn.disabled = true;
                btn.textContent = '⏳ Submitting…';
            }
        }
    });
})();

/* ─── Admin Dashboard — Filter Tabs ────────────────────────────── */
(function () {
    const tabs = document.querySelectorAll('.filter-tab');
    const rows = document.querySelectorAll('.complaint-row');
    if (!tabs.length || !rows.length) return;

    tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
            tabs.forEach(function (t) { t.classList.remove('active'); });
            this.classList.add('active');

            const filter = this.dataset.filter;
            rows.forEach(function (row) {
                if (filter === 'all') {
                    row.style.display = '';
                } else {
                    row.style.display = (row.dataset.status === filter) ? '' : 'none';
                }
            });
        });
    });
})();

/* ─── Track Page — auto-submit if prefill_id is present ─────────── */
(function () {
    const trackForm = document.getElementById('trackForm');
    if (!trackForm) return;

    const input = trackForm.querySelector('input[name="complaint_id"]');
    // If the field was pre-filled (redirected after complaint submission), submit automatically
    if (input && input.value.trim() !== '') {
        // Only auto-submit if not already showing results (no complaint-result div present)
        const alreadyShowing = document.querySelector('.complaint-result');
        if (!alreadyShowing) {
            trackForm.submit();
        }
    }
})();

/* ─── Animate Numbers on Stats Cards ───────────────────────────── */
(function () {
    function animateNumber(el, target) {
        let current = 0;
        const step = Math.ceil(target / 30);
        const timer = setInterval(function () {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = current;
        }, 30);
    }

    // Animate stat-number elements on the page
    document.querySelectorAll('.stat-number, .admin-stat-number').forEach(function (el) {
        const target = parseInt(el.textContent, 10);
        if (!isNaN(target) && target > 0) {
            el.textContent = '0';
            // Trigger after a short delay for visual effect
            setTimeout(function () { animateNumber(el, target); }, 200);
        }
    });
})();
