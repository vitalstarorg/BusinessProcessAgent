import { useState } from 'react';

interface JsonViewerProps {
  data: unknown;
  level?: number;
}

export const JsonViewer = ({ data, level = 0 }: JsonViewerProps) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const isObject = typeof data === 'object' && data !== null && !Array.isArray(data);
  const isArray = Array.isArray(data);
  const hasChildren = isObject || isArray;

  const toggleExpand = () => {
    if (hasChildren) {
      setIsExpanded(!isExpanded);
    }
  };

  const renderValue = (value: unknown): React.ReactNode => {
    if (value === null) return 'null';
    if (typeof value === 'string') return `"${value}"`;
    if (typeof value === 'number') return value;
    if (typeof value === 'boolean') return value.toString();
    if (Array.isArray(value)) return '[]';
    if (typeof value === 'object') return '{}';
    return String(value);
  };

  return (
    <div className="font-mono text-sm">
      {hasChildren ? (
        <>
          <span
            className="cursor-pointer hover:text-blue-500"
            onClick={toggleExpand}
          >
            {isExpanded ? '▼' : '▶'} {isArray ? '[' : '{'}
          </span>
          {isExpanded && (
            <div className="ml-4">
              {Object.entries(data as Record<string, unknown>).map(([key, value], index) => (
                <div key={key} className="flex">
                  <span className="text-blue-500">{key}:</span>
                  {typeof value === 'object' && value !== null ? (
                    <JsonViewer data={value} level={level + 1} />
                  ) : (
                    <span className="ml-2">{renderValue(value)}</span>
                  )}
                </div>
              ))}
            </div>
          )}
          <span>{isArray ? ']' : '}'}</span>
        </>
      ) : (
        <span>{renderValue(data)}</span>
      )}
    </div>
  );
};
