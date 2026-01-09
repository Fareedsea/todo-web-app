export const Footer = () => {
  return (
    <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="md:flex md:items-center md:justify-between">
          <div className="flex justify-center md:justify-start">
            <span className="text-gray-600 dark:text-gray-400 text-sm font-medium">
              © 2026 TaskFlow. All rights reserved.
            </span>
          </div>
          <div className="mt-4 md:mt-0 flex justify-center space-x-8">
            <a
              href="#"
              className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors duration-200 text-sm font-medium"
            >
              Terms of Service
            </a>
            <a
              href="#"
              className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors duration-200 text-sm font-medium"
            >
              Privacy Policy
            </a>
            <a
              href="#"
              className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors duration-200 text-sm font-medium"
            >
              Contact Us
            </a>
          </div>
        </div>
        <div className="mt-6 text-center">
          <p className="text-gray-500 dark:text-gray-500 text-xs">
            Built with ❤️ for productivity enthusiasts everywhere
          </p>
        </div>
      </div>
    </footer>
  );
};