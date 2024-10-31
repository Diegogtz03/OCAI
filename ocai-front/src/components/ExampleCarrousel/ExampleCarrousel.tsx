export const ExampleCarrousel = () => {
  return (
    <div className="flex flex-row overflow-x-scroll gap-5">
      {/* 1 */}
      <div className="bg-gray-100 rounded-md border-gray-300 border p-2 min-w-72 max-w-72">
        <h1 className="text-gray-500 font-bold opacity-75 w-full text-left mb-4">
          Describe your project
        </h1>

        <p className="opacity-50 text-left break-words">
          Let OCAI know what your project is about, what you{"'"}re looking for
          and let the magic happen
        </p>
      </div>

      {/* 2 */}
      <div className="bg-gray-100 rounded-md border-gray-300 border p-2 min-w-72 max-w-72">
        <h1 className="text-gray-500 font-bold opacity-75 w-full text-left mb-4">
          Ask for guidance
        </h1>

        <p className="opacity-50 text-left break-words">
          Ask about a specific questions about the services
        </p>
      </div>

      {/* 3 */}
      <div className="bg-gray-100 rounded-md border-gray-300 border p-2 min-w-72 max-w-72">
        <h1 className="text-gray-500 font-bold opacity-75 w-full text-left mb-4">
          Action Plan
        </h1>

        <p className="opacity-50 text-left break-words">
          Work hands-free allowing OCAI creating your services for you
        </p>
      </div>
    </div>
  );
};
