import React from "react";

export default function CompatibilityScore({ score }) {
  return (
    <div className="mt-5">
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-base font-medium">Compatibility Score</h2>
        <span className="text-sm">{score}%</span>
      </div>
      <div className="relative w-full h-2 rounded bg-neutral-600">
        <div
          className="h-full bg-green-500 rounded"
          style={{ width: `${score}%` }}
          role="progressbar"
          aria-valuenow={score}
          aria-valuemin="0"
          aria-valuemax="100"
        />
      </div>
    </div>
  );
}
