module.exports = function (plop) {
    plop.setGenerator('component', {
      description: 'Créer un composant React',
      prompts: [
        {
          type: 'input',
          name: 'name',
          message: 'Nom du composant ?',
        },
      ],
      actions: [
        {
          type: 'add',
          path: 'src/components/{{pascalCase name}}.jsx',
          templateFile: 'plop-templates/Component.jsx.hbs',
        },
      ],
    });
  };
  