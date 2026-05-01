import React, {useEffect, useState} from 'react'
import { useDispatch } from 'react-redux'
import { setForm, updateField, patchForm, resetForm } from '../redux/slices/formContext.js'

const INTERACTION_TYPES = ["Meeting", "Call", "Email", "Conference", "Virtual"];

function SentimentOption({ value, emoji, label, selected, onChange }) {
  return (
    <button
      type="button"
      onClick={() => onChange(value)}
      className={`flex items-center gap-2 px-4 py-2 rounded-full border text-sm font-medium transition-all duration-150
        ${
          selected
            ? "bg-slate-800 text-white border-slate-800 shadow-md"
            : "bg-white text-slate-500 border-slate-200 hover:border-slate-400 hover:text-slate-700"
        }`}
    >
      <span className="text-base">{emoji}</span>
      {label}
    </button>
  );
}

function TypeDropdown({ value, onChange }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-700 bg-white hover:border-slate-300 flex items-center justify-between transition-all duration-150 focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
      >
        {value}
        <svg
          className={`w-4 h-4 text-slate-400 transition-transform duration-200 ${open ? "rotate-180" : ""}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {open && (
        <div className="absolute z-20 mt-1 w-full bg-white border border-slate-200 rounded-xl shadow-lg overflow-hidden">
          {INTERACTION_TYPES.map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => {
                onChange(t);
                setOpen(false);
              }}
              className={`w-full text-left px-4 py-2.5 text-sm hover:bg-indigo-50 transition-colors ${
                value === t ? "text-indigo-600 font-semibold bg-indigo-50" : "text-slate-700"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function TagInput({ value = [], onAdd, onRemove, placeholder }) {
  const [input, setInput] = useState("");

  const tags = Array.isArray(value) ? value : [];

  const handleKeyDown = (e) => {
    const trimmed = input.trim();

    if ((e.key === "Enter" || e.key === ",") && trimmed) {
      e.preventDefault();

      if (!tags.includes(trimmed)) {
        onAdd?.(trimmed);
      }

      setInput("");
    }
    else if (e.key === "Backspace" && !input && tags.length) {
      onRemove?.(tags[tags.length - 1]);
    }
  };

  const removeTag = (tag) => {
    onRemove?.(tag);
  };

  return (
    <div className="flex flex-wrap gap-1.5 items-center w-full border border-slate-200 rounded-xl px-3 py-2 bg-white hover:border-slate-300 focus-within:border-indigo-400 focus-within:ring-2 focus-within:ring-indigo-100 transition-all min-h-[42px]">
      
      {tags.map((tag, i) => (
        <span
          key={`${tag}-${i}`} 
          className="flex items-center gap-1 bg-indigo-50 text-indigo-700 text-xs font-medium px-2.5 py-1 rounded-full"
        >
          {tag}
          <button
            type="button"
            onClick={() => removeTag(tag)}
            className="text-indigo-400 hover:text-indigo-600"
          >
            ×
          </button>
        </span>
      ))}

      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={tags.length === 0 ? placeholder : ""}
        className="flex-1 min-w-[120px] text-sm text-slate-700 placeholder-slate-400 bg-transparent outline-none"
      />
    </div>
  );
}

function MaterialRow({ label, items, onAdd, onRemove,addLabel, icon }) {
  return (
    <div className="px-4 py-3 flex items-center justify-between">
      <div>
        <p className="text-xs font-semibold text-slate-600 uppercase tracking-wider">{label}</p>
        {items.length === 0 ? (
          <p className="text-xs text-slate-400 mt-0.5 italic">No {label.toLowerCase()} added.</p>
        ) : (
          <ul className="mt-1 space-y-0.5">
            {items.map((item, i) => (
              <li key={i} className="text-xs text-slate-600 flex items-center gap-2">
                <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full inline-block" />
                {item}
                <button
                    type="button"
                    onClick={() => onRemove?.(item)}
                    className="text-slate-400 hover:text-red-500 ml-1"
                >
                    ×
                </button>
                </li>
            ))}
          </ul>
        )}
      </div>
      <button
        type="button"
        onClick={onAdd}
        className="flex items-center gap-1.5 px-3 py-1.5 border border-slate-200 rounded-lg text-xs font-medium text-slate-600 hover:border-slate-400 hover:bg-slate-50 transition-all hover:-translate-y-px active:translate-y-0 shrink-0"
      >
        {icon}
        {addLabel}
      </button>
    </div>
  );
}

function TopicsInput({ value, dispatch, patchForm }) {
  return (
    <TagInput
      value={value}
      onAdd={(tag) =>
        dispatch(patchForm({ topics: { add: [tag] } }))
      }
      onRemove={(tag) =>
        dispatch(patchForm({ topics: { remove: [tag] } }))
      }
      placeholder="Enter topics and press Enter…"
    />
  );
}

function Form({form,   set, handleSubmit, onReset, onSave, onDelete}) {
  const dispatch = useDispatch()
  const inputClass =
    "w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-700 bg-white placeholder-slate-400 transition-all duration-150 hover:border-slate-300 focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100";
  const labelClass = "block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5";

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-200">
        <h2 className="text-lg font-semibold text-black tracking-tight">Interaction Details</h2>
        <p className="text-slate-400 text-xs mt-0.5">Log your HCP engagement</p>
      </div>
      
      {/*Form Content */}
      <form onSubmit={handleSubmit} className="flex-1 overflow-auto px-6 py-5 space-y-5">
        {/* Row 1: HCP Name + Interaction Type */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className={labelClass}>HCP Name</label>
            <input
              type="text"
              placeholder="Search or select HCP…"
              value={form.hcp_name}
              onChange={(e) => set("hcp_name")(e.target.value)}
              className={inputClass}
            />
          </div>
          <div>
            <label className={labelClass}>Interaction Type</label>
            <TypeDropdown value={form.interaction_type} onChange={set("interaction_type")} />
          </div>
        </div>

        {/* Row 2: Date + Time */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className={labelClass}>Date</label>
            <input
              type="date"
              value={form.date}
              onChange={(e) => set("date")(e.target.value)}
              className={inputClass}
            />
          </div>
          <div>
            <label className={labelClass}>Time</label>
            <input
              type="time"
              value={form.time}
              onChange={(e) => set("time")(e.target.value)}
              className={inputClass}
            />
          </div>
        </div>

        {/* Attendees */}
        <div>
          <label className={labelClass}>Attendees</label>
          <TagInput
                value={form.attendees}
                onAdd={(tag) =>
                    dispatch(patchForm({ attendees: { add: [tag] } }))
                }
                onRemove={(tag) =>
                    dispatch(patchForm({ attendees: { remove: [tag] } }))
                }
                placeholder="Enter names and press Enter…"
                />
        </div>

        {/* Topics Discussed */}
        <div>
          <div className="relative">
            <label className={labelClass}>Topics Discussed</label>
            <TopicsInput
                value={form.topics}
                dispatch={dispatch}
                patchForm={patchForm}
            />
          </div>
        </div>

        {/* Materials Shared / Samples Distributed */}
        <div className="border border-slate-200 rounded-xl overflow-hidden divide-y divide-slate-100">
            <MaterialRow
                label="Materials Shared"
                items={form.materials}
                addLabel="Add Materials"
                onAdd={() => {
                    const name = prompt("Enter material name:");
                    if (name) {
                    dispatch(patchForm({ materials: { add: [name] } }));
                    }
                }}
                onRemove={(item) =>
                    dispatch(patchForm({ materials: { remove: [item] } }))
                }
                icon={
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                }
            />
            <MaterialRow
            label="Samples Distributed"
            items={form.samples}
            addLabel="Add Sample"
            onAdd={() => {
                const name = prompt("Enter sample name:");
                if (name) {
                dispatch(patchForm({ samples: { add: [name] } }));
                }
            }}
            onRemove={(item) =>
                dispatch(patchForm({ samples: { remove: [item] } }))
            }
            icon={
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
            }
            />
        </div>

        {/* Sentiment */}
        <div>
          <label className={labelClass}>Observed / Inferred HCP Sentiment</label>
          <div className="flex gap-2 mt-1 flex-wrap">
            <SentimentOption value="positive" emoji="😊" label="Positive" selected={form.sentiment === "positive"} onChange={set("sentiment")} />
            <SentimentOption value="neutral" emoji="😐" label="Neutral" selected={form.sentiment === "neutral"} onChange={set("sentiment")} />
            <SentimentOption value="negative" emoji="😞" label="Negative" selected={form.sentiment === "negative"} onChange={set("sentiment")} />
          </div>
        </div>

        {/* Outcomes */}
        <div>
          <label className={labelClass}>Outcomes</label>
          <textarea
            rows={2}
            placeholder="Key outcomes or agreements…"
            value={form.outcomes}
            onChange={(e) => set("outcomes")(e.target.value)}
            className={`${inputClass} resize-none`}
          />
        </div>

        {/* Follow-up Actions */}
        <div>
          <label className={labelClass}>Follow-up Actions</label>
          <TagInput
                value={form.followUps}
                onAdd={(tag) =>
                    dispatch(patchForm({ followUps: { add: [tag] } }))
                }
                onRemove={(tag) =>
                    dispatch(patchForm({ followUps: { remove: [tag] } }))
                }
                placeholder="Enter next steps or tasks.."
                />
        </div>

        {/*  Buttons */}
        <div className="flex gap-3 pt-4 pb-5">
          <button
            type="button"
            onClick={onDelete}
            className="flex-1 py-2.5 rounded-xl border bg-red-300 border-slate-200 text-sm font-medium text-black hover:bg-red-400 transition-all hover:-translate-y-px active:translate-y-0"
          >
            Delete Form
          </button>
          <button
            type="button"
            onClick={onReset}
            className="flex-1 py-2.5 bg-blue-200 rounded-xl border border-slate-200 text-sm font-medium text-black hover:bg-blue-300 transition-all hover:-translate-y-px active:translate-y-0"
          >
            Reset Form
          </button>
          <button
            type="submit"
            className="flex-1 py-2.5 rounded-xl bg-slate-800 text-white text-sm font-medium hover:bg-slate-700 transition-all hover:-translate-y-px active:translate-y-0 shadow-md"
          >
            Save Interaction
          </button>
        </div>
      </form>
      
    </div>
  );
}

export default Form