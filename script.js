// Navegação suave
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 70;
                window.scrollTo({ top: offsetTop, behavior: 'smooth' });
            }
        });
    });

    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        navbar.style.transform = (scrollTop > lastScrollTop && scrollTop > 100)
            ? 'translateY(-100%)' : 'translateY(0)';
        lastScrollTop = scrollTop;
    });

    const keys = document.querySelectorAll('.key');
    keys.forEach(key => {
        key.addEventListener('click', function() {
            const frequencies = this.getAttribute('data-freq').split(',');
            const digit = this.textContent;
    
            // Efeito visual
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
    
            // Mostrar informações da frequência
            showFrequencyInfo(digit, frequencies);
        });
    });
    

    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.theory-card, .metric-card, .step-content, .chart-container');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    const metricValues = document.querySelectorAll('.metric-value');
    metricValues.forEach(metric => {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        });
        observer.observe(metric);
    });
});

function showFrequencyInfo(digit, frequencies) {
    const tooltip = document.createElement('div');
    tooltip.className = 'frequency-tooltip';
    tooltip.innerHTML = `
        <div class="tooltip-content">
            <h4>Dígito ${digit}</h4>
            <p>Frequência Baixa: ${frequencies[0]} Hz</p>
            <p>Frequência Alta: ${frequencies[1]} Hz</p>
        </div>
    `;
    tooltip.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
        border: 2px solid #3b82f6;
    `;
    document.body.appendChild(tooltip);
    setTimeout(() => { tooltip.style.opacity = '1'; }, 10);
    setTimeout(() => {
        tooltip.style.opacity = '0';
        setTimeout(() => { document.body.removeChild(tooltip); }, 300);
    }, 3000);
}

function animateCounter(element) {
    const target = parseInt(element.textContent);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = element.textContent.includes('%') ? Math.floor(current) + '%' : Math.floor(current);
    }, 16);
}

// Frequências DTMF
const dtmfFrequencies = {
    '1': [697, 1209], '2': [697, 1336], '3': [697, 1477],
    '4': [770, 1209], '5': [770, 1336], '6': [770, 1477],
    '7': [852, 1209], '8': [852, 1336], '9': [852, 1477],
    '*': [941, 1209], '0': [941, 1336], '#': [941, 1477]
};

function tocarDTMF(digito) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const context = new AudioContext();
    const [f1, f2] = dtmfFrequencies[digito];
    const duracao = 0.3;

    const osc1 = context.createOscillator();
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(f1, context.currentTime);

    const osc2 = context.createOscillator();
    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(f2, context.currentTime);

    const gain = context.createGain();
    gain.gain.setValueAtTime(0.2, context.currentTime);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(context.destination);

    osc1.start();
    osc2.start();
    osc1.stop(context.currentTime + duracao);
    osc2.stop(context.currentTime + duracao);
}