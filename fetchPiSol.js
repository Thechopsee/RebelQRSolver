class DataUpdater {
    constructor(endpoint, elementId, interval = 120000) {
        this.endpoint = endpoint;
        this.elementId = elementId;
        this.interval = interval;
        this.intervalId = null;

        this.startAutoRefresh();
    }

    async fetchDataAndUpdateElement() {
        try {
            const response = await fetch(this.endpoint);

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            // Převod odpovědi na JSON
            const data = await response.json();

            // Ověření, zda data obsahují očekávaný klíč 'value'
            if (!data.hasOwnProperty('value')) {
                throw new Error('Chybí klíč "value" v JSON datách');
            }

            // Aktualizace elementu na stránce
            const element = document.getElementById(this.elementId);
            if (element) {
                element.textContent = data.value;
            } else {
                throw new Error(`Element s ID "${this.elementId}" nebyl nalezen`);
            }
        } catch (error) {
            // Zobrazení chyby v konzoli
            console.error('Chyba při získávání dat:', error.message);
        }
    }

    // Metoda pro zahájení automatické aktualizace
    startAutoRefresh() {
        // Inicializace: získání dat hned po startu
        this.fetchDataAndUpdateElement();

        // Nastavení intervalové aktualizace každé 2 minuty (nebo podle zadaného intervalu)
        this.intervalId = setInterval(() => {
            this.fetchDataAndUpdateElement();
        }, this.interval);
    }

    // Metoda pro zastavení automatické aktualizace
    stopAutoRefresh() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
            console.log('Automatická aktualizace zastavena');
        } else {
            console.log('Automatická aktualizace není spuštěna');
        }
    }
}

const updater = new DataUpdater('https://example.com/api', 'element-id');
