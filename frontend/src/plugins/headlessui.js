import {
    Listbox,
    ListboxButton,
    ListboxOption,
    ListboxOptions,
  } from '@headlessui/vue';
  
  export default {
    install(app) {
      app.component('Listbox', Listbox);
      app.component('ListboxButton', ListboxButton);
      app.component('ListboxOption', ListboxOption);
      app.component('ListboxOptions', ListboxOptions);
    }
  };
  